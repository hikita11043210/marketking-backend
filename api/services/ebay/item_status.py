from api.services.ebay.inventory import Inventory
from api.services.ebay.offer import Offer
from api.services.ebay.common import Common
import requests
import logging

logger = logging.getLogger(__name__)

class ItemStatusService(Common):
    """eBayの商品状態を管理するサービスクラス"""
    
    def __init__(self, user):
        super().__init__(user)
        self.inventory_service = Inventory(user)
        self.offer_service = Offer(user)


    def get_item_status(self, sku: str):
        """
        商品の状態を総合的に判定する
        Returns:
            - ACTIVE: 出品中
            - SOLD_OUT: 売り切れ
            - ENDED: 取り下げ
            - NOT_FOUND: 商品が見つからない
        """
        try:
            # 在庫情報の取得
            inventory = self.inventory_service.get_inventory_item_for_sku(sku)
            if inventory is None:
                return None
            quantity = inventory.get('availability', {}).get('shipToLocationAvailability', {}).get('quantity', 0)
            
            # オファー状態の取得
            offer_status = self.offer_service.get_offer_status(sku)
            if offer_status == "PUBLISHED":
                if quantity > 0:
                    return "ACTIVE"  # 出品中で在庫あり
                else:
                    return "SOLD_OUT"  # 出品中だが在庫なし（売り切れ）
            else:
                return "ENDED"  # 取り下げ状態
                
        except Exception as e:
            logger.error(f"商品状態の取得に失敗しました: {str(e)}")
            return None

    def get_item_view_and_watch_count(self):
        """
        商品の閲覧数とウォッチ数を取得する
        Returns:
            dict: 閲覧数とウォッチ数のデータ
        """
        try:
            endpoint = "https://api.ebay.com/sell/analytics/v1/traffic_report"
            headers = self._get_headers()

            # 日付範囲を設定（タイムゾーン考慮のため、昨日までの31日間を指定）
            from datetime import datetime, timedelta
            
            # 今日ではなく昨日を終了日に設定（タイムゾーンの問題を回避）
            end_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
            # 終了日から30日前を開始日に設定（合計31日間）
            start_date = (datetime.now() - timedelta(days=31)).strftime("%Y%m%d")
            
            params = {
                "dimension": "LISTING",
                "metric": "LISTING_VIEWS_TOTAL",
                "filter": f"marketplace_ids:{{{self.marketplace_id}}},date_range:[{start_date}..{end_date}]"
            }

            response = requests.get(endpoint, headers=headers, params=params)
            
            if response.status_code != 200:
                logger.error(f"eBayトラフィックレポートAPIエラー: {response.status_code} - {response.text}")
                return None
            
            result = response.json()
            
            # レポートデータを整形
            report_data = {}
            
            if 'records' in result:
                for record in result['records']:
                    # dimensionValuesから商品ID（ebayId）を取得
                    ebay_id = None
                    if 'dimensionValues' in record and len(record['dimensionValues']) > 0:
                        ebay_id = record['dimensionValues'][0].get('value')
                    
                    if not ebay_id:
                        continue
                    
                    # metricValuesから閲覧数（view）を取得
                    view_count = 0
                    if 'metricValues' in record and len(record['metricValues']) > 0:
                        view_count = int(record['metricValues'][0].get('value', 0))
                    
                    # データを格納
                    report_data[ebay_id] = {
                        'ebayId': ebay_id,
                        'view': view_count
                    }
            
            return report_data
    
        except Exception as e:
            logger.error(f"商品の閲覧数とウォッチ数の取得に失敗しました: {str(e)}")
            return None