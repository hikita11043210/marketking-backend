import time
import logging
from api.models.ebay import Ebay, EbaySKUHistory
from api.services.ebay.inventory import Inventory
from api.services.ebay.offer import Offer
from api.services.ebay.policy import Policy
from django.db import transaction
from api.models.master import Status, YahooAuctionStatus, YahooFreeMarketStatus
from api.models.yahoo import YahooAuction, YahooFreeMarket
from decimal import Decimal
import json

logger = logging.getLogger(__name__)

class SKUManager:
    """
    eBayのSKUを管理するためのサービスクラス
    SKUの生成、履歴管理、再出品処理などを担当する
    """
    def __init__(self, user):
        self.user = user
        self.inventory_service = Inventory(user)
        self.offer_service = Offer(user)
        self.policy_service = Policy(user)
    
    def generate_new_sku(self, original_sku, unique_id):
        """
        再出品用に新しいSKUを生成する
        元のSKUのプレフィックス部分を保持し、タイムスタンプを付与する
        """
        timestamp = time.strftime("%Y%m%d%H%M%S")
        parts = original_sku.split('_')
        
        if len(parts) >= 2:
            # SKUがプレフィックス_IDの形式の場合
            prefix = parts[0]
            return f"{prefix}_{unique_id}_{timestamp}"
        else:
            # 形式が不明な場合はそのままタイムスタンプを付ける
            return f"{original_sku}_{unique_id}_{timestamp}"
    
    def record_sku_history(self, ebay_item, previous_sku, new_sku):
        """
        SKUの変更履歴をデータベースに記録する
        """
        history = EbaySKUHistory(
            ebay=ebay_item,
            previous_sku=previous_sku,
            new_sku=new_sku
        )
        history.save()
        logger.info(f"SKU履歴を記録しました: {previous_sku} → {new_sku}")
        return history
    
    def get_default_policies(self):
        """
        デフォルトのポリシーIDを取得する
        """
        try:
            # 支払いポリシーの取得
            payment_policies = self.policy_service.get_payment_policies().get('paymentPolicies', [])
            payment_policy_id = payment_policies[0]['paymentPolicyId'] if payment_policies else ""
            
            # 返品ポリシーの取得
            return_policies = self.policy_service.get_return_policies().get('returnPolicies', [])
            return_policy_id = return_policies[0]['returnPolicyId'] if return_policies else ""
            
            # 配送ポリシーの取得
            fulfillment_policies = self.policy_service.get_fulfillment_policies().get('fulfillmentPolicies', [])
            fulfillment_policy_id = fulfillment_policies[0]['fulfillmentPolicyId'] if fulfillment_policies else ""
            
            return {
                "paymentPolicyId": payment_policy_id,
                "returnPolicyId": return_policy_id,
                "fulfillmentPolicyId": fulfillment_policy_id
            }
        except Exception as e:
            logger.error(f"デフォルトポリシーの取得に失敗しました: {str(e)}")
            return {
                "paymentPolicyId": "",
                "returnPolicyId": "",
                "fulfillmentPolicyId": ""
            }
    
    def get_category_id_from_offer(self, offers):
        """
        既存のオファーからカテゴリIDを取得
        """
        if offers and len(offers) > 0:
            existing_offer = offers[0]
            if 'categoryId' in existing_offer:
                return existing_offer['categoryId']
        return None
    
    def wait_for_inventory_item(self, sku, max_attempts=5, delay_seconds=5):
        """
        在庫アイテムがeBayシステムに反映されるまで待機する
        
        Args:
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
                inventory_item = self.inventory_service.get_inventory_item_for_sku(sku)
                if inventory_item:
                    logger.info(f"在庫アイテム {sku} が正常に反映されました（試行回数: {attempt + 1}）")
                    # レスポンス内容の詳細をログ出力（デバッグ用）
                    logger.info(f"在庫アイテムのレスポンス詳細: {json.dumps(inventory_item, indent=2)}")
                    return True
                
                # レスポンスの詳細をログ出力（デバッグ用）
                logger.warning(f"在庫アイテム {sku} のレスポンス: {inventory_item}")
                
                # 見つからなかった場合は待機して再試行
                logger.warning(f"在庫アイテム {sku} がまだ反映されていません。待機中...（試行回数: {attempt + 1}/{max_attempts}）")
                time.sleep(delay_seconds)
            except Exception as e:
                logger.error(f"在庫アイテム確認中にエラーが発生しました: {str(e)}")
                # エラーのスタックトレースも出力
                logger.exception("スタックトレース:")
                time.sleep(delay_seconds)
        
        logger.error(f"在庫アイテム {sku} の反映確認が失敗しました（最大試行回数到達）")
        return False
    
    @transaction.atomic
    def republish_with_new_sku(self, old_ebay_item):
        """
        終了済み商品を新しいSKUで再出品する
        1. 新しいSKUを生成
        2. 元の在庫情報を取得
        3. 新しいSKUで在庫情報を作成
        4. 新しいオファーを作成
        5. 新しいEbayレコードを作成
        6. Yahooオークション/フリマのデータを複製して新しいIDを生成
        7. 古いYahooデータのステータスを更新（ID=4）
        8. 古いEbayレコードのステータスを更新（ID=6: 再出品済み）
        9. SKU履歴を記録
        """
        old_sku = old_ebay_item.sku
        if old_ebay_item.yahoo_auction_id:
            old_yahoo_auction = YahooAuction.objects.get(id=old_ebay_item.yahoo_auction_id.id)
            unique_id = old_yahoo_auction.unique_id
        elif old_ebay_item.yahoo_free_market_id:
            old_yahoo_free_market = YahooFreeMarket.objects.get(id=old_ebay_item.yahoo_free_market_id.id)
            unique_id = old_yahoo_free_market.unique_id
        else:
            raise ValueError("Yahooオークション/フリマのデータが見つかりません")
        
        new_sku = self.generate_new_sku(old_sku, unique_id)
        
        logger.info(f"商品を再出品します: 古いSKU={old_sku}, 新しいSKU={new_sku}")
        
        try:
            # 元の在庫情報を取得
            inventory_item = self.inventory_service.get_inventory_item_for_sku(old_sku)
            if not inventory_item:
                raise ValueError(f"在庫情報が見つかりません: SKU={old_sku}")
            
            # デバッグ用に元の在庫情報の詳細をログ出力
            logger.info(f"元の在庫情報の詳細: SKU={old_sku}, データ={json.dumps(inventory_item, indent=2)}")
            
            # 商品説明がない場合は問題となるため、新しく作成する方式に変更
            aspects = {}
            if 'product' in inventory_item and 'aspects' in inventory_item['product']:
                aspects = inventory_item['product']['aspects']
            
            title = "再出品商品"
            if 'product' in inventory_item and 'title' in inventory_item['product']:
                title = inventory_item['product']['title']
            
            description = "This is a relisted item."
            if 'product' in inventory_item and 'description' in inventory_item['product']:
                description = inventory_item['product']['description']
            
            images = []
            if 'product' in inventory_item and 'imageUrls' in inventory_item['product']:
                images = inventory_item['product']['imageUrls']
            
            condition = "USED_EXCELLENT"
            if 'condition' in inventory_item:
                condition = inventory_item['condition']
            
            quantity = 1

            
            # 必要最低限の在庫データを新規作成
            inventory_copy = {
                "availability": {
                    "shipToLocationAvailability": {
                        "quantity": quantity
                    }
                },
                "condition": condition,
                "product": {
                    "title": title,
                    "description": description,
                    "aspects": aspects,
                    "imageUrls": images
                }
            }
            
            # デバッグ用に作成した在庫情報の詳細をログ出力
            logger.info(f"新しい在庫情報の詳細: SKU={new_sku}, データ={json.dumps(inventory_copy, indent=2)}")
            
            # 新しい在庫項目を作成
            self.inventory_service.create_inventory_item(new_sku, inventory_copy)
            logger.info(f"新しい在庫項目を作成しました: SKU={new_sku}")
            
            # 在庫アイテムがeBayシステムに反映されるまで待機
            if not self.wait_for_inventory_item(new_sku):
                raise ValueError(f"新しい在庫アイテム {new_sku} の反映確認ができませんでした。処理を中断します。")
            
            # 元のオファー情報を取得
            existing_offers = self.offer_service.get_offers_by_sku(old_sku)
            
            # デフォルト値の初期化
            policies = {}
            merchant_location_key = ""
            category_id = None
            listing_description = "This is a relisted item."  # デフォルトの説明文
            format_type = "FIXED_PRICE"
            available_quantity = 1
            country_code = "US"
            
            if existing_offers and len(existing_offers) > 0:
                # 既存のオファーからすべての情報を取得
                existing_offer = existing_offers[0]
                
                # ポリシー情報を取得
                if 'listingPolicies' in existing_offer:
                    policies = {
                        "fulfillmentPolicyId": existing_offer['listingPolicies'].get('fulfillmentPolicyId', ''),
                        "paymentPolicyId": existing_offer['listingPolicies'].get('paymentPolicyId', ''),
                        "returnPolicyId": existing_offer['listingPolicies'].get('returnPolicyId', ''),
                    }
                    logger.info(f"既存のオファーからポリシー情報を取得しました: {policies}")
                
                # 出品場所情報を取得
                if 'merchantLocationKey' in existing_offer:
                    merchant_location_key = existing_offer.get('merchantLocationKey', '')
                
                # カテゴリIDを取得
                if 'categoryId' in existing_offer:
                    category_id = existing_offer['categoryId']
                    logger.info(f"既存のオファーからカテゴリIDを取得しました: {category_id}")
                
                # 説明文を取得
                if 'listingDescription' in existing_offer:
                    listing_description = existing_offer['listingDescription']
                    logger.info(f"既存のオファーから説明文を取得しました（長さ: {len(listing_description)}文字）")
                
                # フォーマットタイプを取得
                if 'format' in existing_offer:
                    format_type = existing_offer['format']
                
                # 数量を取得
                if 'availableQuantity' in existing_offer:
                    available_quantity = existing_offer['availableQuantity']
                    # 数量が0以下の場合は1に設定
                    if not isinstance(available_quantity, int) or available_quantity <= 0:
                        available_quantity = 1
                        logger.warning(f"オファーの数量が0以下または無効なため、1に設定しました")
                
                # 国コードを取得
                if 'countryCode' in existing_offer:
                    country_code = existing_offer['countryCode']
            
                if 'pricingSummary' in existing_offer:
                    price = existing_offer['pricingSummary'].get('price', {}).get('value', '')

            # 説明文が無効（空）の場合は在庫情報から取得を試みる
            if not listing_description or listing_description.strip() == "":
                if inventory_item.get("product", {}).get("description"):
                    listing_description = inventory_item["product"]["description"]
                    logger.info(f"在庫情報から説明文を取得しました（長さ: {len(listing_description)}文字）")
                else:
                    # それでも取得できない場合はデフォルトの説明文を設定
                    listing_description = f"This is a relisted item with SKU: {new_sku}."
                    logger.warning(f"説明文が見つからないため、デフォルト説明文を使用します: {listing_description}")
            
            # ポリシー情報がない場合は新しく取得
            if not policies.get('fulfillmentPolicyId') or not policies.get('paymentPolicyId') or not policies.get('returnPolicyId'):
                policies = self.get_default_policies()
                logger.info(f"新しくポリシー情報を取得しました: {policies}")
            
            # 出品場所情報がない場合は新しく取得
            if not merchant_location_key:
                inventory_locations = self.inventory_service.get_inventory_locations()
                if inventory_locations and 'locations' in inventory_locations and len(inventory_locations['locations']) > 0:
                    merchant_location_key = inventory_locations['locations'][0]['merchantLocationKey']
            
            # カテゴリIDが取得できない場合はエラー
            if not category_id:
                if inventory_item.get("product", {}).get("categoryId"):
                    category_id = inventory_item["product"]["categoryId"]
                else:
                    # 先頭のカテゴリIDを使用 (最終手段)
                    # eBayの一般的なカテゴリ (例: その他, 一般商品など)
                    category_id = "1"
                    logger.warning(f"カテゴリIDが見つからないため、デフォルトカテゴリIDを使用します: {category_id}")
            
            # Decimal型を文字列に変換
            # price = str(old_ebay_item.price_dollar) if isinstance(old_ebay_item.price_dollar, Decimal) else old_ebay_item.price_dollar
            
            # 新しいオファーデータを作成
            offer_data = {
                "sku": new_sku,
                "marketplaceId": self.inventory_service.marketplace_id,
                "format": format_type,
                "availableQuantity": available_quantity,
                "categoryId": category_id,
                "listingDescription": listing_description,
                "listingPolicies": {
                    "fulfillmentPolicyId": policies.get("fulfillmentPolicyId", ""),
                    "paymentPolicyId": policies.get("paymentPolicyId", ""),
                    "returnPolicyId": policies.get("returnPolicyId", "")
                },
                "pricingSummary": {
                    "price": {
                        "value": price,
                        "currency": "USD"
                    }
                },
                "merchantLocationKey": merchant_location_key,
                "countryCode": country_code
            }
            
            # オファーデータのログ出力
            logger.info(f"オファーデータを作成: カテゴリID={category_id}, 説明文長さ={len(listing_description)}文字")
            
            # オファーを作成
            offer_result = self.offer_service.create_offer(offer_data)
            offer_id = offer_result.get('offerId')
            if not offer_id:
                raise ValueError("オファーIDが取得できませんでした")
            
            logger.info(f"新しいオファーを作成しました: offer_id={offer_id}")
            
            # 紐づいているYahooオークションデータがある場合は複製
            new_yahoo_auction_id = None
            if old_ebay_item.yahoo_auction_id:
                # 新しいYahooオークションレコードを作成
                new_yahoo_auction = YahooAuction.objects.create(
                    user=self.user,
                    status=old_yahoo_auction.status,  # 同じステータスを設定
                    unique_id=old_yahoo_auction.unique_id,
                    url=old_yahoo_auction.url,
                    item_name=old_yahoo_auction.item_name,
                    item_price=old_yahoo_auction.item_price,
                    shipping=old_yahoo_auction.shipping,
                    end_time=old_yahoo_auction.end_time
                )
                new_yahoo_auction_id = new_yahoo_auction.id
                logger.info(f"新しいYahooオークションレコードを作成しました: id={new_yahoo_auction_id}")
                
                # 古いYahooオークションのステータスを4に更新
                old_yahoo_auction.status = YahooAuctionStatus.objects.get(id=4)  # 4は終了済みステータスを想定
                old_yahoo_auction.save()
                logger.info(f"古いYahooオークションのステータスを4に更新しました: id={old_ebay_item.yahoo_auction_id}")
            
            # 紐づいているYahooフリマデータがある場合は複製
            new_yahoo_free_market_id = None
            if old_ebay_item.yahoo_free_market_id:
                # 新しいYahooフリマレコードを作成
                new_yahoo_free_market = YahooFreeMarket.objects.create(
                    user=self.user,
                    status=old_yahoo_free_market.status,  # 同じステータスを設定
                    unique_id=old_yahoo_free_market.unique_id,
                    url=old_yahoo_free_market.url,
                    item_name=old_yahoo_free_market.item_name,
                    item_price=old_yahoo_free_market.item_price,
                    shipping=old_yahoo_free_market.shipping
                )
                new_yahoo_free_market_id = new_yahoo_free_market.id
                logger.info(f"新しいYahooフリマレコードを作成しました: id={new_yahoo_free_market_id}")
                
                # 古いYahooフリマのステータスを4に更新
                old_yahoo_free_market.status = YahooFreeMarketStatus.objects.get(id=4)  # 4は終了済みステータスを想定
                old_yahoo_free_market.save()
                logger.info(f"古いYahooフリマのステータスを4に更新しました: id={old_ebay_item.yahoo_free_market_id}")
            
            # 新しいEbayレコードを作成
            new_ebay_item = Ebay.objects.create(
                user=self.user,
                sku=new_sku,
                offer_id=offer_id,
                status=Status.objects.get(id=1),  # 出品中のステータス
                product_name=old_ebay_item.product_name,
                price_dollar=old_ebay_item.price_dollar,
                price_yen=old_ebay_item.price_yen,
                shipping_price=old_ebay_item.shipping_price,
                final_profit_dollar=old_ebay_item.final_profit_dollar,
                final_profit_yen=old_ebay_item.final_profit_yen,
                yahoo_auction_id_id=new_yahoo_auction_id,  # 新しく作成したYahooオークションID
                yahoo_free_market_id_id=new_yahoo_free_market_id  # 新しく作成したYahooフリマID
            )
            
            logger.info(f"新しいeBayレコードを作成しました: id={new_ebay_item.id}, SKU={new_sku}")
            
            # 古い商品のステータスを「再出品済み」(id=6)に更新
            old_ebay_item.status = Status.objects.get(id=6)  # 再出品済みステータス
            old_ebay_item.save()
            
            logger.info(f"古い商品のステータスを再出品済み(id=6)に更新しました: id={old_ebay_item.id}, SKU={old_sku}")
            
            # 出品をアクティブ化
            publish_result = self.offer_service.publish_offer(offer_id)
            item_id = publish_result.get('listingId')
            if not item_id:
                raise ValueError("出品IDが取得できませんでした")
            
            # 新しいitem_idを保存
            new_ebay_item.item_id = item_id
            new_ebay_item.url = f"https://www.ebay.com/itm/{item_id}"
            new_ebay_item.save()
            
            logger.info(f"商品を出品しました: item_id={item_id}")
            
            # SKU履歴を記録
            self.record_sku_history(new_ebay_item, old_sku, new_sku)
            
            return {
                'success': True,
                'old_sku': old_sku,
                'new_sku': new_sku,
                'new_ebay_item_id': new_ebay_item.id,
                'new_item_id': item_id,
                'new_offer_id': offer_id,
                'new_yahoo_auction_id': new_yahoo_auction_id,
                'new_yahoo_free_market_id': new_yahoo_free_market_id
            }
            
        except Exception as e:
            logger.error(f"再出品処理中にエラーが発生しました: {str(e)}")
            # エラー発生時、在庫項目が作成されていたら削除を試みる
            try:
                self.inventory_service.delete_inventory_item(new_sku)
                logger.info(f"エラー発生のため在庫項目を削除しました: SKU={new_sku}")
            except Exception as cleanup_error:
                logger.error(f"エラー後の在庫項目削除に失敗しました: {str(cleanup_error)}")
            # トランザクションのロールバックは@transaction.atomicで自動的に行われる
            raise Exception(f"再出品に失敗しました: {str(e)}")
    
    def get_sku_history(self, sku):
        """
        特定のSKUの履歴を取得する
        """
        histories = EbaySKUHistory.objects.filter(
            previous_sku=sku
        ).order_by('-created_at')
        
        return list(histories)
    
    def find_latest_sku(self, original_sku):
        """
        指定されたSKUの最新バージョンを取得する
        """
        current_sku = original_sku
        
        while True:
            next_history = EbaySKUHistory.objects.filter(
                previous_sku=current_sku
            ).order_by('-created_at').first()
            
            if next_history:
                current_sku = next_history.new_sku
            else:
                break
        
        return current_sku 