from api.services.ebay.offer import Offer
from api.models.yahoo import YahooAuction
from api.services.yahoo_auction.scraping import ScrapingService
from api.models.master import Status as StatusModel, YahooAuctionStatus
from api.utils.convert_date import convert_yahoo_date
from django.db import transaction, models
import logging
from api.models.ebay import Ebay
from decimal import Decimal
from django.utils import timezone
from itertools import islice
from api.utils.get_default_user import get_default_user

logger = logging.getLogger(__name__)

class SynchronizeYahooAuction():
    BATCH_SIZE = 10  # 一度に処理するアイテム数

    def __init__(self, user=None):
        self.user = user if user else get_default_user()
        self.scraping_service = ScrapingService()
        self.offer_service = Offer(self.user)

    def _process_batch(self, items, active_status, end_status, ebay_end_status):
        """
        バッチ単位でアイテムを処理
        """
        updated_items = []
        count_active_items = 0
        count_sold_out_items = 0
        count_change_status_items = 0

        for item in items:
            try:
                detail = self.scraping_service.check_item_exist({'url': item.url})
                if detail.get('success') is False:
                    logger.error(f"商品情報の取得に失敗しました - unique_id: {item.unique_id}, エラー: {detail.get('error')}")
                    continue

                old_status_id = item.status.id

                # オークション終了判定
                if detail.get('end_flag'):
                    item.status = end_status

                    # まだ出品中の場合は出品を取り消す
                    if old_status_id == 1:
                        ebay_items = getattr(item, 'prefetched_ebay', [])
                        ebay_item = next((e for e in ebay_items), None)
                        
                        if ebay_item and ebay_item.offer_id:
                            try:
                                self.offer_service.withdraw_offer(ebay_item.offer_id)
                                ebay_item.status = ebay_end_status
                                ebay_item.save()
                            except Exception as e:
                                logger.error(f"eBay出品の取り消しに失敗しました - offer_id: {ebay_item.offer_id}, エラー: {str(e)}")
                        else:
                            logger.warning(f"関連するEbayレコードが見つかりませんでした - Yahoo Auction ID: {item.id}")
                        
                        count_change_status_items += 1
                else:
                    # 価格と終了時間を更新
                    if detail.get('buy_now_price_in_tax'):
                        item.item_price = detail['buy_now_price_in_tax']
                    if detail.get('end_time'):
                        item.end_time = convert_yahoo_date(detail['end_time'])
                    item.status = active_status

                item.save()
                
                # ステータスカウントの更新
                if item.status.id == 1:  # アクティブ
                    count_active_items += 1
                elif item.status.id == 3:  # 終了済み
                    count_sold_out_items += 1
                
                # 更新情報を記録
                if old_status_id != item.status.id:
                    updated_items.append({
                        'unique_id': item.unique_id,
                        'old_status': old_status_id,
                        'new_status': item.status.id
                    })

            except Exception as item_error:
                logger.error(f"Yahooオークションの同期中にエラーが発生しました - unique_id: {item.unique_id}, エラー: {str(item_error)}")
                continue

        return {
            'updated_items': updated_items,
            'count_active_items': count_active_items,
            'count_sold_out_items': count_sold_out_items,
            'count_change_status_items': count_change_status_items
        }

    def synchronize(self, yahoo_auction_item: YahooAuction = None):
        """
        Yahooオークションの商品ステータスを同期する
        """
        try:
            synchronize_start_time = timezone.now()
            total_updated_items = []
            total_active_items = 0
            total_sold_out_items = 0
            total_change_status_items = 0
            
            with transaction.atomic():
                if yahoo_auction_item:
                    yahoo_auction_items = (
                        YahooAuction.objects
                        .select_for_update()
                        .select_related('status')
                        .prefetch_related(
                            models.Prefetch(
                                'ebay_set',
                                queryset=Ebay.objects.select_related('status'),
                                to_attr='prefetched_ebay'
                            )
                        )
                        .filter(id=yahoo_auction_item.id)
                    )
                else:
                    yahoo_auction_items = (
                        YahooAuction.objects
                        .select_for_update()
                        .select_related('status')
                        .prefetch_related(
                            models.Prefetch(
                                'ebay_set',
                                queryset=Ebay.objects.select_related('status'),
                                to_attr='prefetched_ebay'
                            )
                        )
                        .filter(status_id=1)
                    )

                total_items = yahoo_auction_items.count()
                active_status = YahooAuctionStatus.objects.get(id=1)
                end_status = YahooAuctionStatus.objects.get(id=3)
                ebay_end_status = StatusModel.objects.get(id=2)

                # バッチ処理
                it = iter(yahoo_auction_items)
                while True:
                    batch = list(islice(it, self.BATCH_SIZE))
                    if not batch:
                        break

                    result = self._process_batch(batch, active_status, end_status, ebay_end_status)
                    
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
            logger.error(f"Yahooオークションの同期処理でエラーが発生しました: {str(e)}")
            return str(e)