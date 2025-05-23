from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.yahoo_auction.scraping import ScrapingService
import logging
from api.utils.throttles import AuctionDetailThrottle
from api.models import YahooAuction
from api.utils.response_helpers import create_success_response, create_error_response
logger = logging.getLogger(__name__)    

class SearchView(APIView):
    throttle_classes = [AuctionDetailThrottle]

    """
    ヤフオクの商品検索
    """
    def get(self, request):
        try:
            uniques = YahooAuction.objects.all().values('unique_id')
            service = ScrapingService()
            result = service.get_items(request.query_params)

            # 既存のitem_idを除外
            if 'items' in result:
                unique_ids = {item['unique_id'] for item in uniques}  # セットに変換
                result['items'] = [item for item in result['items'] if item['auction_id'] not in unique_ids]
            return create_success_response(
                data=result,
                message='検索が完了しました'
            )
        except ValueError as e:
            return create_error_response(
                e,
                message='検索処理に失敗しました'
            )
        except Exception as e:
            logger.error(f"商品検索でエラーが発生: {str(e)}")
            return create_error_response(
                e,
                message='検索処理に失敗しました'
            )