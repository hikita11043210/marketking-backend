from rest_framework.views import APIView
from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import Ebay
from api.services.currency import CurrencyService
from decimal import Decimal
from api.services.ebay.offer import Offer
from api.services.ebay.inventory import Inventory
from api.services.synchronize.ebay import Status
from api.services.synchronize.yahoo_free_market import SynchronizeYahooFreeMarket
from django.db import transaction
import logging
from django.core.paginator import Paginator
from django.db.models import Q
from api.tasks import sync_yahoo_free_market_manual
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

class YahooFreeMarketListView(APIView):
    def get(self, request):
        try:
            # パラメータを取得
            search = request.query_params.get('search', '')
            sku = request.query_params.get('sku', '')
            status = request.query_params.get('status', '')
            yahoo_status = request.query_params.get('yahoo_status', '')
            limit = int(request.query_params.get('limit', 100))
            page = int(request.query_params.get('page', 1))

            # 商品情報を取得（YahooAuctionとの関連を含める）
            list_items = Ebay.objects.select_related(
                'yahoo_free_market_id',
                'yahoo_free_market_id__status',
                'status'
            ).filter(yahoo_free_market_id__isnull=False).order_by('status', '-update_datetime')

            # 検索フィルタを適用
            if search:
                list_items = list_items.filter(
                    Q(yahoo_free_market_id__item_name__icontains=search) |
                    Q(sku__icontains=search)
                )
            
            if sku:
                list_items = list_items.filter(sku__icontains=sku)
            
            if status:
                list_items = list_items.filter(status__status_name=status)
            
            if yahoo_status:
                list_items = list_items.filter(yahoo_free_market_id__status__status_name=yahoo_status)

            # ページネーションを適用
            paginator = Paginator(list_items, limit)
            current_page = paginator.get_page(page)
            
            # 一覧出力時の変換レートを取得
            rate = Decimal(str(CurrencyService.get_exchange_rate('USD', 'JPY')))

            # 一覧出力時のデータを作成
            items_data = []
            for item in current_page:
                item_data = {
                    'id': item.id,
                    'status': item.status.status_name,
                    'sku': item.sku,
                    'offer_id': item.offer_id,
                    'ebay_price': int(item.price * rate),
                    'ebay_shipping_price': int(item.shipping_price),
                    'final_profit': int(item.final_profit * rate),
                    'view_count': item.view_count,
                    'watch_count': item.watch_count,
                    'yahoo_free_market_id': item.yahoo_free_market_id.id,
                    'yahoo_free_market_unique_id': item.yahoo_free_market_id.unique_id,
                    'yahoo_free_market_url': item.yahoo_free_market_id.url,
                    'yahoo_free_market_item_name': item.yahoo_free_market_id.item_name,
                    'yahoo_free_market_item_price': str(item.yahoo_free_market_id.item_price),
                    'yahoo_free_market_shipping': str(item.yahoo_free_market_id.shipping),
                    'purchase_price': int(item.yahoo_free_market_id.item_price + item.yahoo_free_market_id.shipping),
                    'yahoo_free_market_status': item.yahoo_free_market_id.status.status_name,
                    'insert_datetime': item.insert_datetime,
                    'update_datetime': item.update_datetime
                }
                items_data.append(item_data)

            response_data = {
                'items': items_data,
                'pagination': {
                    'total_count': paginator.count,
                    'total_pages': paginator.num_pages,
                    'current_page': page,
                    'has_next': current_page.has_next(),
                    'has_previous': current_page.has_previous()
                },
                'counts': {
                    'active': list_items.filter(status_id=1).count(),
                    'sold_out': list_items.filter(status_id=2).count(),
                }
            }
            return create_success_response(response_data)
        except Exception as e:
            return create_error_response(str(e))


    def delete(self, request):
        try:
            # パラメータを取得
            sku = request.query_params.get('sku')
            if not sku:
                return create_error_response("SKUが指定されていません")

            # インスタンスを生成
            ebay_service_offer = Offer(request.user)
            ebay_service_inventory = Inventory(request.user)

            # 出品情報を削除
            with transaction.atomic():
                try:
                    # Ebayデータを取得
                    ebay_item = Ebay.objects.select_related('yahoo_free_market_id').get(sku=sku)
                    yahoo_free_market = ebay_item.yahoo_free_market_id
                    
                    # まずeBayの出品を取り下げ
                    if ebay_item.offer_id:
                        ebay_service_offer.withdraw_offer(ebay_item.offer_id)
                    
                    # 次にeBayの在庫を削除
                    ebay_service_inventory.delete_inventory_item(sku)
                    
                    # Ebayデータを先に削除
                    ebay_item.delete()

                    # 最後にYahooFreeMarketのデータを削除（存在する場合）
                    if yahoo_free_market:
                        yahoo_free_market.delete()

                except Ebay.DoesNotExist:
                    return create_error_response("指定されたSKUの商品が見つかりません")
                except Exception as api_error:
                    logger.error(f"eBay APIエラー - SKU: {sku}, エラー: {str(api_error)}")
                    raise

            return create_success_response(message="出品情報を削除しました")
        except Exception as e:
            return create_error_response(str(e))


class SynchronizeYahooFreeMarketView(APIView):
    def get(self, request):
        try:
            # 非同期タスクとして実行
            task = sync_yahoo_free_market_manual.delay(request.user.id)
            
            return Response({
                'status': 'accepted',
                'message': 'Yahoo Free Market同期処理を開始しました',
                'task_id': task.id
            }, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            return create_error_response(str(e))