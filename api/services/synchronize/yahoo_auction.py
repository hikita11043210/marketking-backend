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
logger = logging.getLogger(__name__)

class SynchronizeYahooAuction():
    def __init__(self, user):
        self.user = user

    def synchronize(self):
        """
        eBayの商品ステータスを同期する
        """
        try:
            synchronize_start_time = timezone.now()  # 開始時刻を記録
            updated_items = []
            total_items = 0
            count_active_items = 0
            count_sold_out_items = 0
            count_change_status_items = 0
            
            with transaction.atomic():
                # N+1問題対策のため、関連するEbayデータを事前に取得
                yahoo_auction_items = YahooAuction.objects.select_for_update().filter(status_id=1)
                yahoo_auction_items = yahoo_auction_items.select_related('status').prefetch_related(
                    models.Prefetch(
                        'ebay_set',
                        queryset=Ebay.objects.select_related('status'),
                        to_attr='prefetched_ebay'
                    )
                )
                total_items = yahoo_auction_items.count()
                
                # ステータスオブジェクトを事前に取得（パフォーマンス向上）
                end_status = YahooAuctionStatus.objects.get(id=3)  # 終了済み
                ebay_end_status = StatusModel.objects.get(id=2)  # eBayの終了ステータス
                
                for item in yahoo_auction_items:
                    try:
                        data = ScrapingService().get_item_detail({'url': item.url})

                        if not data:
                            logger.error(f"スクレイピング結果が不正です - unique_id: {item.unique_id}")
                            continue

                        old_status_id = item.status.id
                        
                        # オークション終了判定
                        if data.get('end_flag'):
                            item.status = end_status  # 事前に取得したステータスを使用

                            # まだ出品中の場合は出品を取り消す
                            if old_status_id == 1:
                                offer_service = Offer(self.user)
                                ebay_items = getattr(item, 'prefetched_ebay', [])
                                ebay_item = next((e for e in ebay_items), None)
                                
                                if ebay_item and ebay_item.offer_id:
                                    offer_service.withdraw_offer(ebay_item.offer_id)
                                    ebay_item.status = ebay_end_status
                                    ebay_item.save()
                                else:
                                    logger.warning(f"関連するEbayレコードが見つかりませんでした - Yahoo Auction ID: {item.id}")
                                
                                count_change_status_items += 1
                        else:
                            # 終了日時の更新
                            end_time = convert_yahoo_date(data.get('end_time'))
                            if end_time:
                                item.end_time = end_time
                            
                            # 価格情報の更新
                            if 'current_price' in data and data['current_price']:
                                try:
                                    current_price = float(data['current_price']) if data['current_price'] else 0
                                    item.item_price = current_price
                                except (ValueError, TypeError) as e:
                                    logger.warning(f"現在価格の変換に失敗: {data.get('current_price')} - unique_id: {item.unique_id}, エラー: {str(e)}")
                                    item.item_price = 0
                            elif 'buy_now_price' in data and data['buy_now_price']:
                                try:
                                    buy_now_price = float(data['buy_now_price']) if data['buy_now_price'] else 0
                                    item.item_price = buy_now_price
                                except (ValueError, TypeError) as e:
                                    logger.warning(f"即決価格の変換に失敗: {data.get('buy_now_price')} - unique_id: {item.unique_id}, エラー: {str(e)}")
                                    item.item_price = 0

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

                synchronize_end_time = timezone.now()  # 終了時刻を記録

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
            logger.error(f"Yahooオークションの同期処理でエラーが発生しました: {str(e)}")
            return str(e)