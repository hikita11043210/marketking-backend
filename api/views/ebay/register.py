from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.services.ebay.inventory import Inventory
from api.services.ebay.offer import Offer
from api.models.ebay import EbayRegisterFromYahooAuction
from api.models.master import Status, Condition
from api.utils.throttles import AuctionDetailThrottle
from api.utils.response_helpers import create_success_response, create_error_response
from api.utils.generate_log_file import generate_log_file
from decimal import Decimal
import logging
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)

class EbayRegisterView(APIView):
    """eBayに商品を出品するView"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuctionDetailThrottle]

    def post(self, request):
        """
        eBayに商品を出品するエンドポイント
        """
        try:
            product_data = request.data['product_data']
            yahoo_auction_data = request.data['yahoo_auction_data']
            other_data = request.data['other_data']

            # 重複チェック
            if EbayRegisterFromYahooAuction.objects.filter(yahoo_auction_id=yahoo_auction_data['yahoo_auction_id'], status__id=1).exists():
                return create_error_response("すでに出品済みの商品です")

            # SKUの生成（yahoo_auction_idを使用）
            sku = f"YA_{yahoo_auction_data['yahoo_auction_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            # itemSpecificsを変換
            aspects = {}
            for item in product_data['itemSpecifics']['nameValueList']:
                aspects[item['name']] = item['value']

            # ConditionEnumを取得するAPIが無いので、文字列を変換して条件を設定
            # https://developer.ebay.com/api-docs/sell/inventory/types/slr:ConditionEnum
            condition_enum = (
                product_data['condition']['conditionDescription']
                .upper()        # 全大文字に変換（例: "like new" → "LIKE NEW"）
                .replace(" ", "_")  # スペースをアンダースコアに置換（例: "LIKE NEW" → "LIKE_NEW"）
            )

            condition_enum = Condition.objects.get(condition_id=product_data['condition']['conditionId']).condition_enum

            # 商品情報の構築
            register_data = {
                "availability": {
                    "shipToLocationAvailability": {
                        "quantity": product_data['quantity']
                    }
                },
                "condition": condition_enum,
                "product": {
                    "title": product_data['title'],
                    "description": product_data['description'],
                    "aspects": aspects,
                    "imageUrls": product_data['images']
                }
            }

            # Inventoryのインスタンス化
            ebay_service_inventory = Inventory(request.user)

            # 商品情報の登録
            ebay_service_inventory.create_inventory_item(sku, register_data)

            # ロケーション情報を取得
            inventory_locations = ebay_service_inventory.get_inventory_locations()

            # 出品情報の作成（価格などの情報を自動設定）
            offer_data = {
                "sku": sku,
                "marketplaceId": settings.EBAY_MARKETPLACE_ID,
                "format": "FIXED_PRICE",
                "categoryId": product_data['categoryId'],
                "listingDescription": product_data['description'],
                "listingPolicies": {
                    "fulfillmentPolicyId": product_data['shippingPolicyId'],
                    "paymentPolicyId": product_data['paymentPolicyId'],
                    "returnPolicyId": product_data['returnPolicyId']
                },
                "pricingSummary": {
                    "price": {
                        "value": product_data['price'],
                        "currency": "USD"
                    }
                },
                "countryCode": "US",
                "merchantLocationKey": inventory_locations['locations'][0]['merchantLocationKey']
            }

            # 出品情報の作成
            ebay_service_offer = Offer(request.user)
            offer_result = ebay_service_offer.create_offer(offer_data)
            
            # 出品のアクティブ化
            ebay_service_offer.publish_offer(offer_result['offerId'])

            # データの保存
            status_obj = Status.objects.get(id=1)
            EbayRegisterFromYahooAuction.objects.create(
                user=request.user,
                sku=sku,
                offer_id=offer_result['offerId'],
                status=status_obj,
                ebay_price=Decimal(str(product_data['price'])),
                ebay_shipping_price=Decimal(str(other_data['ebay_shipping_price'] if other_data['ebay_shipping_price'] else settings.EBAY_SHIPPING_COST)),
                final_profit=Decimal(str(other_data['final_profit'])),
                yahoo_auction_id=yahoo_auction_data['yahoo_auction_id'],
                yahoo_auction_url=yahoo_auction_data['yahoo_auction_url'],
                yahoo_auction_item_name=yahoo_auction_data['yahoo_auction_item_name'],
                yahoo_auction_item_price=Decimal(str(yahoo_auction_data['yahoo_auction_item_price'])),
                yahoo_auction_shipping=Decimal(str(yahoo_auction_data['yahoo_auction_shipping'])),
                yahoo_auction_end_time=yahoo_auction_data['yahoo_auction_end_time']
            )

            return create_success_response(
                data=None,
                message='商品の出品が完了しました'
            )

        except Exception as e:
            status_obj = Status.objects.get(id=6)
            EbayRegisterFromYahooAuction.objects.create(
                user=request.user,
                sku=sku,
                offer_id=offer_result['offerId'] if offer_result['offerId'] else None,
                status=status_obj,
                ebay_price=Decimal(str(product_data['price'])),
                ebay_shipping_price=Decimal(str(other_data['ebay_shipping_price'] if other_data['ebay_shipping_price'] else settings.EBAY_SHIPPING_COST)),
                final_profit=Decimal(str(other_data['final_profit'])),
                yahoo_auction_id=yahoo_auction_data['yahoo_auction_id'],
                yahoo_auction_url=yahoo_auction_data['yahoo_auction_url'],
                yahoo_auction_item_name=yahoo_auction_data['yahoo_auction_item_name'],
                yahoo_auction_item_price=Decimal(str(yahoo_auction_data['yahoo_auction_item_price'])),
                yahoo_auction_shipping=Decimal(str(yahoo_auction_data['yahoo_auction_shipping'])),
                yahoo_auction_end_time=yahoo_auction_data['yahoo_auction_end_time']
            )
            generate_log_file(str(e), "yahoo_auction_register", time=True)
            return create_error_response("商品登録に失敗しました。\n詳細はエラーログを確認してください。")