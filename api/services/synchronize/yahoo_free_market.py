from api.services.ebay.offer import Offer
from api.models.yahoo import YahooFreeMarket
from api.services.yahoo_free_market.scraping import ScrapingService
from api.models.master import Status as StatusModel, YahooFreeMarketStatus
from api.utils.convert_date import convert_yahoo_date
from django.db import transaction
from django.utils import timezone
import logging
from api.models.ebay import Ebay
import time

logger = logging.getLogger(__name__)

class SynchronizeYahooFreeMarket():
    def __init__(self, user):
        self.user = user

    def synchronize(self):
        """
        Yahooフリーマーケットの商品ステータスを同期する
        """
        try:
            synchronize_start_time = timezone.now()
            updated_items = []
            total_items = 0
            count_active_items = 0
            count_sold_out_items = 0
            count_change_status_items = 0
            
            with transaction.atomic():
                # statusとebayの関連を事前に取得
                yahoo_free_market_items = (
                    YahooFreeMarket.objects
                    .select_for_update()
                    .select_related('status')
                    .prefetch_related(
                        'ebay_set__status'  # Ebayモデルとそのstatusを事前に取得
                    )
                    .filter(status_id=1)
                )

                total_items = yahoo_free_market_items.count()
                # ステータスオブジェクトを事前に取得
                yahoo_end_status = YahooFreeMarketStatus.objects.get(id=3)  # 終了済み
                ebay_end_status = StatusModel.objects.get(id=2)  # eBayの終了ステータス

                for item in yahoo_free_market_items:
                    try:
                        result = ScrapingService().check_item_exist({'item_id': item.unique_id})
                        time.sleep(3)  # 連続アクセスによるタイムアウトを防ぐため3秒待機

                        #  商品が存在しない場合
                        if result:
                            old_status = item.status.id
                            item.status = yahoo_end_status

                            # ebay_setはprefetch_relatedで取得済みなので、first()を使用
                            ebay_item = item.ebay_set.first()
                            if ebay_item and ebay_item.status.id == 1:
                                offer_service = Offer(self.user)
                                offer_service.withdraw_offer(ebay_item.offer_id)
                                ebay_item.status = ebay_end_status
                                ebay_item.save()
                        
                            item.save()
                            
                            # 更新情報を記録
                            updated_items.append({
                                'unique_id': item.unique_id,
                                'old_status': old_status,
                                'new_status': item.status.id,
                            })

                            # ステータス変更のカウント
                            if old_status == 1 and item.status.id == 3:
                                count_change_status_items += 1

                            # 現在のステータスに基づいてカウント
                            if item.status.id == 1:  # アクティブ
                                count_active_items += 1
                            elif item.status.id == 3:  # 終了済み
                                count_sold_out_items += 1
                    
                    except Exception as item_error:
                        logger.error(f"Yahooフリーマーケットの同期中にエラーが発生しました - アイテムID: {item.unique_id}, エラー: {str(item_error)}")
                        continue

            synchronize_end_time = timezone.now()

            return {
                'synchronize_start_time': synchronize_start_time,
                'synchronize_end_time': synchronize_end_time,
                'synchronize_target_item': total_items,
                'count_active_item': count_active_items,
                'count_sold_out_item': count_sold_out_items,
                'count_change_status_item': count_change_status_items,
                'updated_count': len(updated_items),
                'updated_items': updated_items
            }
            
        except Exception as e:
            logger.error(f"Yahooフリーマーケットの同期処理でエラーが発生しました: {str(e)}")
            return str(e)