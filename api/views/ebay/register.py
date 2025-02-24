from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.services.ebay.inventory import Inventory
from api.services.ebay.offer import Offer
from api.models.ebay import EbayRegisterFromYahooAuction
from api.models.master import Status, Condition, Setting, YahooAuctionStatus
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
        eBayに商品を出品する処理
        """
        try:
            # フロントから送信されたデータを取得
            product_data = request.data['product_data']
            yahoo_auction_data = request.data['yahoo_auction_data']
            other_data = request.data['other_data']

            # インスタンスを生成
            ebay_service_inventory = Inventory(request.user)
            ebay_service_offer = Offer(request.user)

            # 二重登録防止の重複チェック
            if EbayRegisterFromYahooAuction.objects.filter(yahoo_auction_id=yahoo_auction_data['yahoo_auction_id'], status__id=1).exists():
                return create_error_response("すでに出品済みの商品です")

            # SKUの生成（yahoo_auction_idを使用）
            sku = f"YA_{yahoo_auction_data['yahoo_auction_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            # itemSpecificsを登録データ用に変換
            aspects = {}
            for item in product_data['itemSpecifics']['nameValueList']:
                aspects[item['name']] = item['value']

            # condition_enumを取得
            # condition_enumを取得するAPIが存在しないため、下記の情報をテーブル化し、カテゴリから取得したcondition_idをもとに取得する
            # https://developer.ebay.com/api-docs/sell/static/metadata/condition-id-values.html
            condition_enum = Condition.objects.get(condition_id=product_data['condition']['conditionId']).condition_enum

            # Settingからdescriptionを取得
            description_template_1 = Setting.objects.get(user=request.user).description_template_1
            description_template_2 = Setting.objects.get(user=request.user).description_template_2
            description_template_3 = Setting.objects.get(user=request.user).description_template_3

            # descriptionを作成
            if product_data['description'] == "":
                description = description_template_1 + description_template_2 + description_template_3
            else:
                description = description_template_1 + product_data['description'] + description_template_3

            # 説明が4000文字以内であることを確認
            if len(description) > 4000:
                return create_error_response("説明が4000文字を超えています")

            # 登録商品情報の構築
            register_data = {
                "availability": {
                    "shipToLocationAvailability": {
                        "quantity": product_data['quantity']
                    }
                },
                "condition": condition_enum,
                "product": {
                    "title": product_data['title'],
                    "description": description,
                    "aspects": aspects,
                    "imageUrls": product_data['images']
                }
            }

            # 商品情報の登録処理
            ebay_service_inventory.create_inventory_item(sku, register_data)

            # ロケーション情報を取得
            # 初回は存在しなかったので新規登録を行った（発送元の住所）
            inventory_locations = ebay_service_inventory.get_inventory_locations()

            # 出品情報の作成（価格などの情報を自動設定）
            offer_data = {
                "sku": sku,
                "marketplaceId": settings.EBAY_MARKETPLACE_ID,
                "format": "FIXED_PRICE",
                "categoryId": product_data['categoryId'],
                "listingDescription": description,
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

            # 出品情報の作成（この時点ではebayに掲載されない】
            offer_result = ebay_service_offer.create_offer(offer_data)
            
            # 出品のアクティブ化（ebayに掲載される）
            ebay_service_offer.publish_offer(offer_result['offerId'])

            # データの保存
            status_obj = Status.objects.get(id=1)
            EbayRegisterFromYahooAuction.objects.create(
                user=request.user,
                sku=sku,
                offer_id=offer_result['offerId'],
                status=status_obj,
                ebay_price=Decimal(str(product_data['price'])),
                ebay_shipping_price=Decimal(str(other_data['ebay_shipping_price'] if other_data['ebay_shipping_price'] else settings.EBAY_SHIPPING_COST)), # 後ほど送料もフロントから送ってくるつもりだが、今は固定値なので環境変数を必ず参照するようにしている
                final_profit=Decimal(str(other_data['final_profit'])),
                yahoo_auction_id=yahoo_auction_data['yahoo_auction_id'],
                yahoo_auction_url=yahoo_auction_data['yahoo_auction_url'],
                yahoo_auction_item_name=yahoo_auction_data['yahoo_auction_item_name'],
                yahoo_auction_item_price=Decimal(str(yahoo_auction_data['yahoo_auction_item_price'])),
                yahoo_auction_shipping=Decimal(str(yahoo_auction_data['yahoo_auction_shipping'])),
                yahoo_auction_end_time=yahoo_auction_data['yahoo_auction_end_time'],
                yahoo_auction_status=YahooAuctionStatus.objects.get(id=1)
            )

            return create_success_response(
                data=None,
                message='商品の出品が完了しました'
            )

        except Exception as e:
            # ebay側にゴミデータが残らないように削除する
            ebay_service_inventory.delete_inventory_item(sku)
            # エラー時の内容をログ出力
            generate_log_file(str(e), "yahoo_auction_register", date=True)
            return create_error_response("商品登録に失敗しました。詳細はエラーログを確認してください。")