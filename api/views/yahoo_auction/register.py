from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.yahoo_auction.scraping import ScrapingService
from rest_framework.permissions import IsAuthenticated
from api.services.ebay.inventory import Inventory
from api.services.ebay.offer import Offer
from api.models.ebay import Ebay
from api.models.master import Status, Condition, Setting, YahooAuctionStatus
from api.models.yahoo import YahooAuction
from api.utils.throttles import AuctionDetailThrottle
from api.utils.response_helpers import create_success_response, create_error_response
from decimal import Decimal
import logging
from django.conf import settings
from datetime import datetime
from django.db import transaction
from api.services.ai.ai import Ai
from api.services.ebay.inventory import Inventory
from api.services.ebay.offer import Offer
from api.services.ebay.trading import Trading
from api.services.ebay.category import Category
from api.services.ai.ai import Ai
from api.services.calculator import CalculatorService
from api.services.translator import TranslatorService
from api.services.ebay.marketplace import Marketplace
import time

logger = logging.getLogger(__name__)

class ItemDetailView(APIView):
    """
    ヤフオクの商品詳細API
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
            logging.info(f"Yahooフリーマーケットの詳細情報取得開始")
            result = service.get_item_detail(request.query_params)
            logging.info(f"Yahooフリーマーケットの詳細情報取得完了")

            # 商品詳細の値セット
            title = result['title']
            description = result['description']
            descriptionHtml = result['descriptionHtml']
            condition = result['condition']
            price = int(result['buy_now_price_in_tax'])
            shipping = int(request.query_params.get('shipping'))

            # カテゴリツリーIDの取得
            logging.info(f"カテゴリツリーIDの取得開始")
            category_tree_id = ebay_service_category.get_categories_tree_id()
            logging.info(f"カテゴリツリーIDの取得完了")

            # キーワードの取得
            logging.info(f"キーワードの取得開始")
            keywords = ai.get_keywords(title)
            logging.info(f"キーワードの取得完了")

            # カテゴリを取得
            logging.info(f"カテゴリの取得開始")
            category = ebay_service_category.get_categories(category_tree_id, keywords)
            logging.info(f"カテゴリの取得完了")

            # カテゴリIDを取得
            logging.info(f"カテゴリIDの取得開始")
            category_id = ai.get_category_id(category, title)
            logging.info(f"カテゴリIDの取得完了")

            # カテゴリ固有の仕様を取得
            logging.info(f"カテゴリ固有の仕様の取得開始")
            category_aspects = trading_api.get_category_aspects(
                category_id=category_id,
                category_tree_id=category_tree_id
            )
            logging.info(f"カテゴリ固有の仕様の取得完了")

            # 商品詳細の取得
            logging.info(f"商品詳細の取得開始")
            item_specifics = ai.extract_cameras_specifics(title, category_aspects, descriptionHtml)
            logging.info(f"商品詳細の取得完了")

            # 商品の状態の説明の取得
            logging.info(f"商品の状態の説明の取得開始")
            condition_description_en = translator_service.translate_text(condition, 'EN-US')
            logging.info(f"商品の状態の説明の取得完了")

            # カテゴリのコンディション情報を取得
            logging.info(f"カテゴリのコンディション情報の取得開始")
            conditions = ebay_service_marketplace.get_category_conditions(category_id)
            logging.info(f"カテゴリのコンディション情報の取得完了")
            selected_condition = 3000

            # 価格計算
            # price = calculator_service.calc_price_dollar(price, shipping, 0)

            data = {
                'item_details': result,
                'title_en': item_specifics['title_en'],
                'title_ja': item_specifics['title_ja'],
                'description_en': item_specifics['description_en'],
                'description_ja': item_specifics['description_ja'],
                'item_specifics': item_specifics['specifics'],
                'category': category,
                'category_id': category_id,
                'condition_description_en': condition_description_en,
                'price': '',
                'conditions': conditions,
                'selected_condition': selected_condition
            }
            return create_success_response(
                data=data,
                message='商品詳細を取得しました'
            )

        except Exception as e:
            print(item_specifics)
            logging.error(f"商品詳細取得中にエラーが発生しました: {str(e)}")
            return create_error_response(
                e,
                message="商品の詳細を取得できませんでした"
            )


def wait_for_inventory_item(inventory_service, sku, max_attempts=3, delay_seconds=2):
    """
    在庫アイテムがeBayシステムに反映されるまで待機する
    
    Args:
        inventory_service: Inventoryサービスのインスタンス
        sku: 確認する商品のSKU
        max_attempts: 最大試行回数
        delay_seconds: 試行間の待機秒数
        
    Returns:
        bool: 在庫アイテムが見つかったかどうか
    """
    logger.info(f"在庫アイテム {sku} の反映を待機中...")
    
    # まず最初に固定で待機
    time.sleep(delay_seconds)
    
    for attempt in range(max_attempts):
        try:
            # 在庫アイテムの取得を試みる
            inventory_item = inventory_service.get_inventory_item_for_sku(sku)
            if inventory_item:
                logger.info(f"在庫アイテム {sku} が正常に反映されました（試行回数: {attempt + 1}）")
                return True
            
            # 見つからなかった場合は待機して再試行
            logger.warning(f"在庫アイテム {sku} がまだ反映されていません。待機中...（試行回数: {attempt + 1}/{max_attempts}）")
            time.sleep(delay_seconds)
        except Exception as e:
            logger.error(f"在庫アイテム確認中にエラーが発生しました: {str(e)}")
            time.sleep(delay_seconds)
    
    logger.error(f"在庫アイテム {sku} の反映確認が失敗しました（最大試行回数到達）")
    return False


class RegisterView(APIView):
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
            if YahooAuction.objects.filter(unique_id=yahoo_auction_data['yahoo_auction_id'], status__id=1).exists():
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

            # # Settingからdescriptionを取得
            # description_template_1 = Setting.objects.get(user=request.user).description_template_1
            # description_template_2 = Setting.objects.get(user=request.user).description_template_2
            # description_template_3 = Setting.objects.get(user=request.user).description_template_3

            # # descriptionを作成
            # if product_data['description'] == "":
            #     description = description_template_1 + description_template_2 + description_template_3
            # else:
            #     # descriptionの各行を<p>タグで囲む
            #     formatted_description = '\n'.join([f'<p>{line}</p>' for line in product_data['description'].split('\n') if line.strip()])
            #     description = description_template_1 + formatted_description + description_template_3

            # 説明が4000文字以内であることを確認
            if len(product_data['description']) > 4000:
                return create_error_response("説明が4000文字を超えています")

            # 登録商品情報の構築
            register_data = {
                "availability": {
                    "shipToLocationAvailability": {
                        "quantity": product_data['quantity']
                    }
                },
                "condition": condition_enum,
                "conditionDescription":product_data['conditionDescription'],
                "product": {
                    "title": product_data['title'],
                    "description": product_data['description'],
                    "aspects": aspects,
                    "imageUrls": product_data['images']
                }
            }

            # 商品情報の登録処理
            ebay_service_inventory.create_inventory_item(sku, register_data)
            logger.info(f"新しい在庫項目を作成しました: SKU={sku}")
            
            # 在庫アイテムがeBayシステムに反映されるまで待機
            if not wait_for_inventory_item(ebay_service_inventory, sku):
                # 反映されなかった場合は削除を試みて終了
                try:
                    ebay_service_inventory.delete_inventory_item(sku)
                    logger.info(f"在庫項目反映失敗のため削除しました: SKU={sku}")
                except Exception as cleanup_error:
                    logger.error(f"在庫項目削除に失敗しました: {str(cleanup_error)}")
                return create_error_response("在庫項目の作成が完了しませんでした。再度お試しください。")

            # ロケーション情報を取得
            # 初回は存在しなかったので新規登録を行った（発送元の住所）
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

            # 出品情報の作成（この時点ではebayに掲載されない】
            offer_result = ebay_service_offer.create_offer(offer_data)
            
            # 出品のアクティブ化（ebayに掲載される）
            publish_result = ebay_service_offer.publish_offer(offer_result['offerId'])
            item_id = publish_result['listingId']  # これがeBayの商品ID

            with transaction.atomic():
                # Yahooオークションのデータを保存
                yahoo_auction = YahooAuction.objects.create(
                    user=request.user,
                    status=YahooAuctionStatus.objects.get(id=1),
                    unique_id=yahoo_auction_data['yahoo_auction_id'],
                    url=yahoo_auction_data['yahoo_auction_url'],
                    item_name=yahoo_auction_data['yahoo_auction_item_name'],
                    item_price=Decimal(str(yahoo_auction_data['yahoo_auction_item_price'])),
                    shipping=Decimal(str(yahoo_auction_data['yahoo_auction_shipping'])),
                    end_time=yahoo_auction_data['yahoo_auction_end_time'],
                    insert_user=request.user,
                    update_user=request.user
                )

                # ebayのデータを保存
                Ebay.objects.create(
                    user=request.user,
                    sku=sku,
                    offer_id=offer_result['offerId'],
                    status=Status.objects.get(id=1),
                    product_name=product_data['title'],
                    url=f"https://www.ebay.com/itm/{item_id}",
                    quantity=product_data['quantity'],
                    price_dollar=Decimal(str(other_data['calculated_price_dollar'])),
                    price_yen=Decimal(str(other_data['calculated_price_yen'])),
                    shipping_price=Decimal(str(other_data['shipping_cost'])),
                    final_profit_dollar=Decimal(str(other_data['final_profit_dollar'])),
                    final_profit_yen=Decimal(str(other_data['final_profit_yen'])),
                    yahoo_auction_id=yahoo_auction,
                    item_id=item_id,
                    insert_user=request.user,
                    update_user=request.user
                )

            return create_success_response(
                data=None,
                message='商品の出品が完了しました'
            )

        except Exception as e:
            # ebay側にゴミデータが残らないように削除する
            try:
                ebay_service_inventory.delete_inventory_item(sku)
                logger.info(f"エラー発生のため在庫項目を削除しました: SKU={sku}")
            except Exception as cleanup_error:
                logger.error(f"エラー後の在庫項目削除に失敗しました: {str(cleanup_error)}")
                
            # エラー時の内容をログ出力
            logger.error(f"商品登録処理でエラーが発生しました: {str(e)}")
            return create_error_response("商品登録に失敗しました。詳細はエラーログを確認してください。")