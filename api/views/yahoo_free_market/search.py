from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.yahoo_free_market.scraping import ScrapingService
import logging
from api.utils.throttles import AuctionDetailThrottle
from api.utils.response_helpers import create_success_response, create_error_response
logger = logging.getLogger(__name__)    

class YahooFreeMarketSearchView(APIView):
    throttle_classes = [AuctionDetailThrottle]

    """
    Yahooフリーマーケットの商品検索
    """
    def get(self, request):
        try:
            service = ScrapingService()
            result = service.get_items(request.query_params)
            return create_success_response(
                data=result,
                message='検索が完了しました'
            )
        except ValueError as e:
            return create_error_response(
                message=str(e)
            )
        except Exception as e:
            logger.error(f"商品検索でエラーが発生: {str(e)}")
            return create_error_response(
                message='検索処理に失敗しました'
            )