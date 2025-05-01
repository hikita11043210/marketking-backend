from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.utils.response_helpers import create_success_response, create_error_response
from api.models.master import Status
from api.models.ebay import Ebay
from api.models.yahoo import YahooAuction
from api.models.sales import Sales
from api.models.purchases import Purchase
from api.services.ebay.offer import Offer
from api.services.ebay.sku_manager import SKUManager
from api.services.synchronize.ebay import Status as SyncStatus
from api.services.synchronize.yahoo_auction import SynchronizeYahooAuction
from api.services.synchronize.yahoo_free_market import SynchronizeYahooFreeMarket
from decimal import Decimal
from django.db import transaction
import logging
from django.utils import timezone
from datetime import datetime

logger = logging.getLogger(__name__)


class WithdrawItemView(APIView):
    """
    商品の取下げを行うView
    ebay上でEndedに更新し、ebayのテーブルステータスを取下げ(id=2)に変更
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # リクエストデータを取得
            sku = request.data.get('sku')

            if not sku:
                return create_error_response("SKUが指定されていません")

            # ebayのデータを取得
            try:
                ebay_register_item = Ebay.objects.get(sku=sku)
            except Ebay.DoesNotExist:
                return create_error_response(f"指定されたSKU({sku})の商品が見つかりません")

            # サービスを初期化
            offer_service = Offer(request.user)

            # 商品を取下げ（「終了済み」に変更）
            if ebay_register_item.item_id:
                offer_service.end_fixed_price_item(ebay_register_item.item_id)
            else:
                return create_error_response(f"item_idが見つかりません: SKU={sku}")
            # ステータスを更新
            ebay_register_item.status = Status.objects.get(id=2)  # 取下げステータス
            ebay_register_item.save()

            return create_success_response(
                data=None,
                message=f'商品を正常に取下げました（SKU: {sku}）'
            )
            
        except Exception as e:
            logger.error(f"商品取下げ処理でエラーが発生しました: {str(e)}")
            return create_error_response(str(e))


class RepublishItemView(APIView):
    """
    商品の再出品を行うView
    SKUを更新してebay上で再出品を行い、ebayのテーブルステータスを出品中(id=1)に変更
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # リクエストデータを取得
            sku = request.data.get('sku')
            
            if not sku:
                return create_error_response("SKUが指定されていません")

            # ebayのデータを取得
            try:
                ebay_register_item = Ebay.objects.get(sku=sku)
            except Ebay.DoesNotExist:
                return create_error_response(f"指定されたSKU({sku})の商品が見つかりません")

            # サービスを初期化
            sku_manager = SKUManager(request.user)
            
            # 商品を再出品（新しいSKUを生成して再出品）
            try:
                # 商品を再出品
                result = sku_manager.republish_with_new_sku(ebay_register_item)
                
                return create_success_response({
                    'message': '新しいSKUで再出品しました',
                    'old_sku': result['old_sku'],
                    'new_sku': result['new_sku'],
                    'new_item_id': result['new_item_id']
                })
            except Exception as republish_error:
                logger.error(f"再出品に失敗しました: {str(republish_error)}")
                return create_error_response(f"再出品に失敗しました: {str(republish_error)}")
                
        except Exception as e:
            logger.error(f"再出品処理でエラーが発生しました: {str(e)}")
            return create_error_response(str(e))


class PurchaseRegistrationView(APIView):
    """
    仕入情報を登録するView
    Yahooのテーブルステータスを仕入済(id=2)に変更
    Yahooデータに紐づいた仕入データを作成
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # リクエストデータを取得
            sku = request.data.get('sku')
            
            if not sku:
                return create_error_response("SKUが指定されていません")

            # ebayのデータを取得
            try:
                ebay_item = Ebay.objects.select_related(
                    'yahoo_auction_id',
                    'yahoo_free_market_id'
                ).get(sku=sku)
            except Ebay.DoesNotExist:
                return create_error_response(f"指定されたSKU({sku})の商品が見つかりません")

            # Yahoo商品情報を取得
            yahoo_item = None
            yahoo_status_id = None
            
            if ebay_item.yahoo_auction_id:
                yahoo_item = ebay_item.yahoo_auction_id
                yahoo_status_id = 2  # 仕入済ステータスID
            elif ebay_item.yahoo_free_market_id:
                yahoo_item = ebay_item.yahoo_free_market_id
                yahoo_status_id = 2  # 仕入済ステータスID
            else:
                return create_error_response("Yahoo商品情報が見つかりません")

            with transaction.atomic():
                # Yahooのステータスを更新
                yahoo_item.status_id = yahoo_status_id
                yahoo_item.save()
                
                # 仕入データを作成
                purchase = Purchase.objects.create(
                    ebay_id_id=ebay_item.id,
                    transaction_date=timezone.now().date(),
                    product_name=yahoo_item.item_name,
                    url=yahoo_item.url,
                    quantity=1,
                    price=yahoo_item.item_price,
                    shipping_cost=yahoo_item.shipping,
                    total_amount=yahoo_item.item_price + yahoo_item.shipping,
                    insert_user=request.user,
                    update_user=request.user
                )

            return create_success_response(
                data={
                    'purchase_id': purchase.id,
                    'product_name': purchase.product_name,
                    'price': str(purchase.price),
                    'shipping_cost': str(purchase.shipping_cost),
                    'total_amount': str(purchase.total_amount),
                    'transaction_date': purchase.transaction_date.isoformat()
                },
                message='仕入情報を登録しました'
            )
            
        except Exception as e:
            logger.error(f"仕入登録処理でエラーが発生しました: {str(e)}")
            return create_error_response(str(e))


class SynchronizeItemView(APIView):
    """
    商品情報を同期するView
    ebayとyahooのデータをそれぞれ同期処理を行う
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # リクエストデータを取得
            sku = request.data.get('sku')
            sync_type = request.data.get('type', 'all')  # all, ebay, yahoo
            
            if not sku:
                return create_error_response("SKUが指定されていません")

            # ebayのデータを取得
            try:
                ebay_item = Ebay.objects.select_related(
                    'yahoo_auction_id',
                    'yahoo_free_market_id'
                ).get(sku=sku)
            except Ebay.DoesNotExist:
                return create_error_response(f"指定されたSKU({sku})の商品が見つかりません")

            result = {}
            
            # 同期対象によって処理を分岐
            if sync_type in ['all', 'ebay']:
                # eBay情報を同期
                ebay_sync = SyncStatus(request.user)
                ebay_result = ebay_sync.synchronize(ebay_item)
                result['ebay'] = ebay_result
            
            if sync_type in ['all', 'yahoo']:
                # Yahoo情報を同期
                if ebay_item.yahoo_auction_id:
                    yahoo_sync = SynchronizeYahooAuction(request.user)
                    yahoo_result = yahoo_sync.synchronize(ebay_item.yahoo_auction_id.id)
                    result['yahoo_auction'] = yahoo_result
                elif ebay_item.yahoo_free_market_id:
                    yahoo_sync = SynchronizeYahooFreeMarket(request.user)
                    yahoo_result = yahoo_sync.synchronize(ebay_item.yahoo_free_market_id.id)
                    result['yahoo_free_market'] = yahoo_result

            return create_success_response(
                data=result,
                message='商品情報の同期が完了しました'
            )
            
        except Exception as e:
            logger.error(f"同期処理でエラーが発生しました: {str(e)}")
            return create_error_response(str(e))


class SalesRegistrationView(APIView):
    """
    売上情報を登録するView
    ebayのテーブルステータスを完了(id=5)に変更
    ebayデータに紐づいた売上データを作成
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # リクエストデータを取得
            sku = request.data.get('sku')
            
            if not sku:
                return create_error_response("SKUが指定されていません")

            # ebayのデータを取得
            try:
                ebay_item = Ebay.objects.select_related('status').get(sku=sku)
            except Ebay.DoesNotExist:
                return create_error_response(f"指定されたSKU({sku})の商品が見つかりません")

            # 重複チェック - 既に売上データが登録されていないか確認
            sales_exists = Sales.objects.filter(management_code=sku).exists()
            if sales_exists:
                return create_error_response(f"このSKU({sku})の売上は既に登録されています")

            with transaction.atomic():
                # ebayのステータスを完了に更新
                ebay_item.status = Status.objects.get(id=4)  # 完了ステータスID
                ebay_item.save()
                
                # 売上データを作成
                sale = Sales.objects.create(
                    ebay_id_id=ebay_item.id,
                    transaction_date=timezone.now().date(),
                    product_name=ebay_item.product_name,
                    management_code=ebay_item.sku,
                    url=ebay_item.url,
                    quantity=ebay_item.quantity,
                    price=ebay_item.price_yen,
                    shipping_cost=ebay_item.shipping_price,
                    total_amount=ebay_item.price_yen - ebay_item.shipping_price,
                    insert_user=request.user,
                    update_user=request.user
                )

            return create_success_response(
                data={
                    'sale_id': sale.id,
                    'product_name': sale.product_name,
                    'price': str(sale.price),
                    'shipping_cost': str(sale.shipping_cost),
                    'total_amount': str(sale.total_amount),
                    'transaction_date': sale.transaction_date.isoformat()
                },
                message='売上情報を登録しました'
            )
            
        except Exception as e:
            logger.error(f"売上登録処理でエラーが発生しました: {str(e)}")
            return create_error_response(str(e)) 