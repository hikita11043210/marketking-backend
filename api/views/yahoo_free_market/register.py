from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.yahoo_free_market.scraping import ScrapingService
from rest_framework.permissions import IsAuthenticated
from api.services.ebay.inventory import Inventory
from api.services.ebay.offer import Offer
from api.models.ebay import Ebay
from api.models.master import Status, Condition, Setting, YahooFreeMarketStatus
from api.models.yahoo import YahooFreeMarket
from api.utils.throttles import AuctionDetailThrottle
from api.utils.response_helpers import create_success_response, create_error_response
from decimal import Decimal
import logging
from django.conf import settings
from datetime import datetime
from django.db import transaction
from api.services.ebay.trading import Trading
from api.services.ebay.category import Category
from api.services.ai.ai import Ai
from api.services.translator import TranslatorService
from api.services.calculator import CalculatorService
from api.services.ebay.marketplace import Marketplace

logger = logging.getLogger(__name__)

class YahooFreeMarketItemDetailView(APIView):
    """
    ヤフオクフリーマーケットの商品詳細取得API
    """
    def get(self, request):
        try:
            # インスタンスを生成
            service = ScrapingService()
            ai = Ai()
            trading_api = Trading(request.user)
            ebay_service_category = Category(request.user)
            translator_service = TranslatorService(request.user)
            calculator_service = CalculatorService(request.user)
            ebay_service_marketplace = Marketplace(request.user)

            # Yahooフリーマーケットの詳細情報取得
            result = service.get_item_detail(request.query_params)

            # 商品詳細の値セット
            title = result['title']
            description = result['description']
            condition = result['condition']
            price = result['price']

            # カテゴリツリーIDの取得
            category_tree_id = ebay_service_category.get_categories_tree_id()

            # カテゴリを取得
            category = ebay_service_category.get_categories(category_tree_id, title)

            # カテゴリIDを取得
            category_id = ai.get_category_id(category, title)

            # カテゴリ固有の仕様を取得
            category_aspects = trading_api.get_category_aspects(
                category_id=category_id,
                category_tree_id=category_tree_id
            )

            # 商品詳細の取得
            item_specifics = ai.extract_cameras_specifics(title, category_aspects, description)

            # 商品の状態の説明の取得
            condition_description_en = translator_service.translate_text(condition, 'EN-US')

            # カテゴリのコンディション情報を取得
            conditions = ebay_service_marketplace.get_category_conditions(category_id)
            selected_condition = 3000

            # 価格計算
            price = calculator_service.calc_price_dollar([price,0])

            data = {
                'item_details': result,
                'item_specifics': item_specifics,
                'category': category,
                'category_id': category_id,
                'condition_description_en': condition_description_en,
                'price': price,
                'conditions': conditions,
                'selected_condition': selected_condition
            }
            return create_success_response(
                data=data,
                message='商品詳細を取得しました'
            )

        except Exception as e:
            return create_error_response(
                e,
                message="商品の詳細を取得できませんでした"
            )



class YahooFreeMarketRegisterView(APIView):
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
            yahoo_free_market_data = request.data['yahoo_free_market_data']
            other_data = request.data['other_data']

            # インスタンスを生成
            ebay_service_inventory = Inventory(request.user)
            ebay_service_offer = Offer(request.user)

            # 二重登録防止の重複チェック
            if YahooFreeMarket.objects.filter(unique_id=yahoo_free_market_data['yahoo_free_market_id'], status__id=1).exists():
                return create_error_response("すでに出品済みの商品です")

            # SKUの生成（yahoo_auction_idを使用）
            sku = f"YFM_{yahoo_free_market_data['yahoo_free_market_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

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
                # descriptionの各行を<p>タグで囲む
                formatted_description = '\n'.join([f'<p>{line}</p>' for line in product_data['description'].split('\n') if line.strip()])
                description = description_template_1 + formatted_description + description_template_3

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
            publish_result = ebay_service_offer.publish_offer(offer_result['offerId'])
            item_id = publish_result['listingId']  # これがeBayの商品ID

            with transaction.atomic():
                # Yahooフリーマーケットのデータを保存
                yahoo_free_market = YahooFreeMarket.objects.create(
                    user=request.user,
                    status=YahooFreeMarketStatus.objects.get(id=1),
                    unique_id=yahoo_free_market_data['yahoo_free_market_id'],
                    url=settings.YAHOO_FREE_MARKET_ITEM_URL + yahoo_free_market_data['yahoo_free_market_id'],
                    item_name=yahoo_free_market_data['yahoo_free_market_item_name'],
                    item_price=Decimal(str(yahoo_free_market_data['yahoo_free_market_item_price'])),
                    shipping=Decimal(str(yahoo_free_market_data['yahoo_free_market_shipping'])),
                )

                # ebayのデータを保存
                Ebay.objects.create(
                    user=request.user,
                    sku=sku,
                    item_id=item_id,
                    offer_id=offer_result['offerId'],
                    status=Status.objects.get(id=1),
                    price=Decimal(str(product_data['price'])),
                    shipping_price=Decimal(str(other_data['ebay_shipping_price'] if other_data['ebay_shipping_price'] else settings.EBAY_SHIPPING_COST)), # 後ほど送料もフロントから送ってくるつもりだが、今は固定値なので環境変数を必ず参照するようにしている
                    final_profit=Decimal(str(other_data['final_profit'])),
                    yahoo_free_market_id=yahoo_free_market
                )

            return create_success_response(
                data=None,
                message='商品の出品が完了しました'
            )

        except Exception as e:
            # ebay側にゴミデータが残らないように削除する
            ebay_service_inventory.delete_inventory_item(sku)
            # エラー時の内容をログ出力
            return create_error_response("商品登録に失敗しました。詳細はエラーログを確認してください。" + str(e))