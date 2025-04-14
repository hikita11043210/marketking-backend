from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.yahoo_free_market.scraping import ScrapingService
import logging
from api.utils.throttles import AuctionDetailThrottle
from api.utils.response_helpers import create_success_response, create_error_response
logger = logging.getLogger(__name__)    
from api.models import YahooFreeMarket
class YahooFreeMarketSearchView(APIView):
    throttle_classes = [AuctionDetailThrottle]

    """
    Yahooフリーマーケットの商品検索
    """
    def get(self, request):
        try:
            uniques = YahooFreeMarket.objects.all().values('unique_id')
            service = ScrapingService()
            result = service.get_items(request.query_params)
            
            # 既存のitem_idを除外
            if 'items' in result:
                unique_ids = {item['unique_id'] for item in uniques}  # セットに変換
                result['items'] = [item for item in result['items'] if item['item_id'] not in unique_ids]

            return create_success_response(
                data=result,
                message='検索が完了しました'
            )
        except ValueError as e:
            return create_error_response(
                message=str(e)
            )
        except Exception as e:
            return create_error_response(
                e,
                message='検索処理に失敗しました'
            )