from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.yahoo_auction.scraping import ScrapingService
import logging
from api.utils.throttles import AuctionDetailThrottle

logger = logging.getLogger(__name__)    

class SearchView(APIView):
    throttle_classes = [AuctionDetailThrottle]

    """
    Yahooフリーマーケットの商品検索
    """
    def get(self, request):
        try:
            service = ScrapingService()
            result = service.get_items(request.query_params)
            return Response({
                'success': True,
                'message': '検索が完了しました',
                'data': result
            })
        except ValueError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"商品検索でエラーが発生: {str(e)}")
            return Response({
                'success': False,
                'message': '検索処理に失敗しました'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)