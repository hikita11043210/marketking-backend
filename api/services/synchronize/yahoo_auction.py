from api.services.ebay.offer import Offer
from api.models.yahoo import YahooAuction
from api.services.yahoo_auction.scraping import ScrapingService
from api.models.master import Status as StatusModel, YahooAuctionStatus
from api.utils.convert_date import convert_yahoo_date
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

class SynchronizeYahooAuction():
    def __init__(self, user):
        self.user = user

    def synchronize(self):
        """
        eBayの商品ステータスを同期する
        """
        try:
            updated_items = []
            total_items = 0
            
            with transaction.atomic():
                yahoo_auction_items = YahooAuction.objects.select_for_update().filter(status_id=1)
                total_items = yahoo_auction_items.count()
                
                for item in yahoo_auction_items:
                    try:
                        scraping_result = ScrapingService().get_item_detail({'url': item.yahoo_auction_url})
                        
                        if not scraping_result or 'data' not in scraping_result:
                            logger.error(f"スクレイピング結果が不正です - SKU: {item.sku}")
                            continue

                        data = scraping_result['data']
                        
                        # オークション終了判定
                        if data.get('end_flag', False):
                            item.yahoo_auction_status = YahooAuctionStatus.objects.get(id=3)  # 終了済み

                            # まだ出品中の場合は出品を取り消す
                            if item.status.id == 1:
                                offer_service = Offer(self.user)
                                offer_service.withdraw_offer(item.offer_id)
                                item.status = StatusModel.objects.get(id=2)
                        else:
                            # 終了日時の更新
                            end_time = convert_yahoo_date(data.get('end_time'))
                            if end_time:
                                item.yahoo_auction_end_time = end_time
                        
                        item.save()
                        
                        # 更新情報を記録
                        updated_items.append({
                            'sku': item.sku,
                            'old_status': item.yahoo_auction_status_id,
                            'new_status': item.yahoo_auction_status_id,
                            'end_time': end_time if not data.get('end_flag', False) else None
                        })
                    
                    except Exception as item_error:
                        logger.error(f"Yahooオークションの同期中にエラーが発生しました - SKU: {item.sku}, エラー: {str(item_error)}")
                        continue

            return {
                    'total_items': total_items,
                    'updated_count': len(updated_items),
                    'updated_items': updated_items
                }
            
        except Exception as e:
            logger.error(f"Yahooオークションの同期処理でエラーが発生しました: {str(e)}")
            return str(e)