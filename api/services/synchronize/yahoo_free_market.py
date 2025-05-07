from api.services.ebay.offer import Offer
from api.models.yahoo import YahooFreeMarket
from api.services.yahoo_free_market.scraping import ScrapingService
from api.models.master import Status as StatusModel, YahooFreeMarketStatus
from api.utils.convert_date import convert_yahoo_date
from django.db import transaction
from django.utils import timezone
import logging
from api.models.ebay import Ebay
from itertools import islice
from api.utils.get_default_user import get_default_user
logger = logging.getLogger(__name__)

class SynchronizeYahooFreeMarket():
    BATCH_SIZE = 10  # 一度に処理するアイテム数

    def __init__(self, user=None):
        self.user = user if user else get_default_user()
        self.scraping_service = ScrapingService()

    def _process_batch(self, items, yahoo_end_status, ebay_end_status):
        """
        バッチ単位でアイテムを処理
        """
        updated_items = []
        count_active_items = 0
        count_sold_out_items = 0
        count_change_status_items = 0

        for item in items:
            try:
                result = self.scraping_service.check_item_exist({'item_id': item.unique_id})

                logger.info(f"---------------------------------------------")
                logger.info(f"Yahooフリーマーケット名: {item.item_name}")
                logger.info(f"YahooフリーマーケットURL: {item.url}")
                logger.info(f"ebaySKU: {item.unique_id}")

                if result:
                    old_status = item.status.id
                    item.status = yahoo_end_status

                    ebay_item = item.ebay_set.first()
                    if ebay_item and ebay_item.status.id == 1:
                        offer_service = Offer(self.user)
                        offer_service.end_fixed_price_item(ebay_item.item_id)
                        ebay_item.status = ebay_end_status
                        ebay_item.save()

                    item.save()

                    updated_items.append({
                        'unique_id': item.unique_id,
                        'old_status': old_status,
                        'new_status': item.status.id,
                    })

                    if old_status == 1 and item.status.id == 3:
                        count_change_status_items += 1

                if item.status.id == 1:
                    count_active_items += 1
                elif item.status.id == 3:
                    count_sold_out_items += 1

            except Exception as item_error:
                logger.error(f"Yahooフリーマーケットの同期中にエラーが発生しました - アイテムID: {item.unique_id}, エラー: {str(item_error)}")
                continue

        return {
            'updated_items': updated_items,
            'count_active_items': count_active_items,
            'count_sold_out_items': count_sold_out_items,
            'count_change_status_items': count_change_status_items
        }

    def synchronize(self, yahoo_free_market_id: int = None):
        """
        Yahooフリーマーケットの商品ステータスを同期する
        """
        try:
            synchronize_start_time = timezone.now()
            total_updated_items = []
            total_active_items = 0
            total_sold_out_items = 0
            total_change_status_items = 0
            
            with transaction.atomic():
                if yahoo_free_market_id:
                    yahoo_free_market_items = (
                        YahooFreeMarket.objects
                        .select_for_update()
                        .select_related('status')
                        .prefetch_related('ebay_set__status')
                        .filter(id=yahoo_free_market_id)
                    )
                else:
                    yahoo_free_market_items = (
                        YahooFreeMarket.objects
                        .select_for_update()
                        .select_related('status')
                        .prefetch_related('ebay_set__status')
                        .filter(status_id=1)
                    )

                total_items = yahoo_free_market_items.count()
                yahoo_end_status = YahooFreeMarketStatus.objects.get(id=3)
                ebay_end_status = StatusModel.objects.get(id=2)

                # バッチ処理
                it = iter(yahoo_free_market_items)
                while True:
                    batch = list(islice(it, self.BATCH_SIZE))
                    if not batch:
                        break

                    result = self._process_batch(batch, yahoo_end_status, ebay_end_status)
                    
                    total_updated_items.extend(result['updated_items'])
                    total_active_items += result['count_active_items']
                    total_sold_out_items += result['count_sold_out_items']
                    total_change_status_items += result['count_change_status_items']

            synchronize_end_time = timezone.now()

            return {
                'synchronize_start_time': synchronize_start_time,
                'synchronize_end_time': synchronize_end_time,
                'synchronize_target_item': total_items,
                'count_active_item': total_active_items,
                'count_sold_out_item': total_sold_out_items,
                'count_change_status_item': total_change_status_items,
                'updated_count': len(total_updated_items),
                'updated_items': total_updated_items
            }
            
        except Exception as e:
            logger.error(f"Yahooフリーマーケットの同期処理でエラーが発生しました: {str(e)}")
            return str(e)