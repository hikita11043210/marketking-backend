from rest_framework.views import APIView
from api.utils.response_helpers import create_success_response, create_error_response
from api.models.ebay import Ebay
from api.services.currency import CurrencyService
from decimal import Decimal
from api.services.ebay.offer import Offer
from api.utils.generate_log_file import generate_log_file
from api.services.ebay.inventory import Inventory
from api.services.synchronize.ebay import Status
from api.services.synchronize.yahoo_auction import SynchronizeYahooAuction
from api.tasks import sync_yahoo_auction_manual
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

class YahooAuctionListView(APIView):
    def get(self, request):
        try:
            # パラメータを取得
            search = request.query_params.get('search', '')
            sku = request.query_params.get('sku', '')
            status_param = request.query_params.get('status', '')
            yahoo_status = request.query_params.get('yahoo_status', '')
            limit = int(request.query_params.get('limit', 20))
            page = int(request.query_params.get('page', 1))
            
            # 商品情報を取得（YahooAuctionとの関連を含める）
            list_items = Ebay.objects.select_related(
                'yahoo_auction_id',
                'yahoo_auction_id__status',
                'status'
            ).filter(yahoo_auction_id__isnull=False, insert_user=request.user).order_by('status', '-update_datetime')
            
            # 検索フィルタを適用
            if search:
                list_items = list_items.filter(
                    Q(yahoo_auction_id__item_name__icontains=search) |
                    Q(sku__icontains=search)
                )
            
            if sku:
                list_items = list_items.filter(sku__icontains=sku)
            
            if status_param:
                try:
                    # カンマ区切りの場合は複数のステータスでフィルタリング
                    status_list = [int(s.strip()) for s in status_param.split(',') if s.strip()]
                    if status_list:
                        list_items = list_items.filter(status_id__in=status_list)
                except Exception as e:
                    logger.error(f"ステータスフィルタエラー: {str(e)}")
            
            if yahoo_status:
                try:
                    # カンマ区切りの場合は複数のステータスでフィルタリング
                    yahoo_status_list = [int(s.strip()) for s in yahoo_status.split(',') if s.strip()]
                    if yahoo_status_list:
                        list_items = list_items.filter(yahoo_auction_id__status_id__in=yahoo_status_list)
                except Exception as e:
                    logger.error(f"Yahooステータスフィルタエラー: {str(e)}")

            # ページネーションを適用
            paginator = Paginator(list_items, limit)
            current_page = paginator.get_page(page)

            # 一覧出力時のデータを作成
            items_data = []
            for item in current_page:
                item_data = {
                    'ebay_id': item.id,
                    'ebay_status': item.status.status_name,
                    'ebay_sku': item.sku,
                    'ebay_offer_id': item.offer_id,
                    'ebay_price_dollar': item.price_dollar,
                    'ebay_price_yen': item.price_yen,
                    'ebay_shipping_price': item.shipping_price,
                    'ebay_final_profit_dollar': item.final_profit_dollar,
                    'ebay_final_profit_yen': item.final_profit_yen,
                    'ebay_view_count': item.view_count,
                    'ebay_watch_count': item.watch_count,
                    'ya_id': item.yahoo_auction_id.id,
                    'ya_unique_id': item.yahoo_auction_id.unique_id,
                    'ya_url': item.yahoo_auction_id.url,
                    'ya_item_name': item.yahoo_auction_id.item_name,
                    'ya_item_price': str(item.yahoo_auction_id.item_price),
                    'ya_shipping': str(item.yahoo_auction_id.shipping),
                    'ya_purchase_amount': int(item.yahoo_auction_id.item_price + item.yahoo_auction_id.shipping),
                    'ya_end_time': item.yahoo_auction_id.end_time.isoformat(),
                    'ya_status': item.yahoo_auction_id.status.status_name,
                    'insert_datetime': item.insert_datetime,
                    'update_datetime': item.update_datetime
                }
                items_data.append(item_data)
            
            # ステータス別集計（フィルタ適用前の全体データから集計）
            all_items = Ebay.objects.filter(yahoo_auction_id__isnull=False, insert_user=request.user)
            
            # フィルタを適用（検索フィルタのみ適用し、ステータスフィルタは適用しない）
            if search:
                all_items = all_items.filter(
                    Q(yahoo_auction_id__item_name__icontains=search) |
                    Q(sku__icontains=search)
                )
            
            if sku:
                all_items = all_items.filter(sku__icontains=sku)

            # スタータス別件数を取得
            active_count = all_items.filter(status__status_name='出品中').count()
            sold_out_count = all_items.filter(status__status_name='売却').count()
            completed_count = all_items.filter(status__status_name='完了').count()
            purchase_available_count = all_items.filter(yahoo_auction_id__status__status_name='仕入可').count()
            purchase_unavailable_count = all_items.filter(yahoo_auction_id__status__status_name='仕入不可').count()
            
            logger.info(f"集計: active={active_count}, sold_out={sold_out_count}, completed={completed_count}, purchase_available={purchase_available_count}, purchase_unavailable={purchase_unavailable_count}")
            
            # ステータスごとの商品数を追加
            response_data = {
                'items': items_data,
                'pagination': {
                    'total_count': paginator.count,
                    'total_pages': paginator.num_pages,
                    'current_page': page,
                    'has_next': current_page.has_next(),
                    'has_previous': current_page.has_previous()
                },
                'counts': {
                    'active': active_count,
                    'sold_out': sold_out_count,
                    'completed': completed_count,
                    'purchase_available': purchase_available_count,
                    'purchase_unavailable': purchase_unavailable_count,
                }
            }
            return create_success_response(response_data)
        except Exception as e:
            logger.error(f"YahooAuctionListView error: {str(e)}", exc_info=True)
            return create_error_response(str(e))

class SynchronizeYahooAuctionView(APIView):
    def get(self, request):
        try:
            # 非同期タスクとして実行
            task = sync_yahoo_auction_manual.delay(request.user.id)
            
            return Response({
                'status': 'accepted',
                'message': 'Yahoo Auction同期処理を開始しました',
                'task_id': task.id
            }, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            return create_error_response(str(e))