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

    def _process_batch(self, ebay_items, active_status, end_status, ebay_end_status):
        """
        バッチ単位でアイテムを処理
        """
        updated_items = []
        count_active_items = 0
        count_sold_out_items = 0
        count_change_status_items = 0

        for ebay_item in ebay_items:
            try:
                # YahooAuctionを取得
                yahoo_auction = ebay_item.yahoo_auction_id
                if not yahoo_auction:
                    logger.warning(f"関連するYahooオークションが見つかりませんでした - SKU: {ebay_item.sku}")
                    continue
                logger.info(f"------------------------------------------------------------------------------------------")
                logger.info(f"Yahoo名前: {yahoo_auction.item_name}")
                logger.info(f"YahooURL: {yahoo_auction.url}")
                logger.info(f"ebaySKU: {yahoo_auction.unique_id}")
                
                detail = self.scraping_service.check_item_exist({'url': yahoo_auction.url})
                if detail.get('success') is False:
                    logger.error(f"商品情報の取得に失敗しました - unique_id: {yahoo_auction.unique_id}, エラー: {detail.get('error')}")
                    continue

                old_status_id = yahoo_auction.status.id

                # オークション終了判定
                if detail.get('end_flag'):
                    yahoo_auction.status = end_status

                    # まだ出品中の場合は出品を取り消す
                    if old_status_id == 1:
                        try:
                            self.offer_service.end_fixed_price_item(ebay_item.item_id)
                            logger.info(f"出品取消SKU: {ebay_item.sku}") 
                            ebay_item.status = ebay_end_status
                            ebay_item.save()
                            logger.info(f"出品取消完了")
                        except Exception as e:
                            logger.error(f"eBay出品の取り消しに失敗しました - offer_id: {ebay_item.offer_id}, エラー: {str(e)}")
                        
                        count_change_status_items += 1
                else:
                    yahoo_auction.status = active_status

                    # 価格と終了時間を更新
                    if detail.get('buy_now_price_in_tax'):
                        price_value = Decimal(str(detail['buy_now_price_in_tax']))
                        logger.info(f"価格更新: {price_value}")
                        logger.info(f"Yahoo価格変更前: {yahoo_auction.item_price}")
                        if yahoo_auction.item_price != price_value:
                            yahoo_auction.item_price = price_value
                            logger.info(f"Yahoo価格変更後: {yahoo_auction.item_price}")
                        else:
                            logger.info(f"価格に変更なし")
                    
                    if detail.get('end_time'):
                        end_time = convert_yahoo_date(detail['end_time'])
                        logger.info(f"終了時間更新: {end_time}")
                        logger.info(f"Yahoo終了時間変更前: {yahoo_auction.end_time}")
                        # タイムゾーン情報を含めて比較するために文字列化
                        if str(yahoo_auction.end_time) != str(end_time):
                            yahoo_auction.end_time = end_time
                            logger.info(f"Yahoo終了時間変更後: {yahoo_auction.end_time}")
                        else:
                            logger.info(f"終了時間に変更なし")

                yahoo_auction.save()
                
                # ステータスカウントの更新
                if yahoo_auction.status.id == 1:  # アクティブ
                    count_active_items += 1
                elif yahoo_auction.status.id == 3:  # 終了済み
                    count_sold_out_items += 1
                
                # 更新情報を記録
                if old_status_id != yahoo_auction.status.id:
                    updated_items.append({
                        'unique_id': yahoo_auction.unique_id,
                        'old_status': old_status_id,
                        'new_status': yahoo_auction.status.id
                    })
                logger.info(f"---------------------------------------------")
            except Exception as item_error:
                logger.error(f"Yahooオークションの同期中にエラーが発生しました - SKU: {ebay_item.sku}, エラー: {str(item_error)}")
                continue

        return {
            'updated_items': updated_items,
            'count_active_items': count_active_items,
            'count_sold_out_items': count_sold_out_items,
            'count_change_status_items': count_change_status_items
        }

    def synchronize(self, yahoo_auction_id: int = None):
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
                if yahoo_auction_id:
                    # 特定のYahooオークションIDに紐づくEbayアイテムを取得
                    ebay_items = (
                        Ebay.objects
                        .select_for_update()
                        .select_related('status', 'yahoo_auction_id', 'yahoo_auction_id__status')
                        .filter(status_id=1, yahoo_auction_id=yahoo_auction_id)
                    )
                else:
                    # ステータスが1（出品中）のEbayアイテムを取得
                    ebay_items = (
                        Ebay.objects
                        .select_for_update()
                        .select_related('status', 'yahoo_auction_id', 'yahoo_auction_id__status')
                        .filter(status_id=1)
                        .filter(yahoo_auction_id__isnull=False)
                    )

                total_items = ebay_items.count()
                logger.info(f"同期対象のeBay商品数: {total_items}")
                
                active_status = YahooAuctionStatus.objects.get(id=1)
                end_status = YahooAuctionStatus.objects.get(id=3)
                ebay_end_status = StatusModel.objects.get(id=2)

                # バッチ処理
                it = iter(ebay_items)
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