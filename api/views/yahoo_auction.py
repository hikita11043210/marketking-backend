from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.yahoo_auction.scraping import ScrapingService
import logging
from api.utils.throttles import AuctionDetailThrottle

logger = logging.getLogger(__name__)    

class ItemSearchView(APIView):
    throttle_classes = [AuctionDetailThrottle]

    """
    ヤフオクの商品検索API
    """
    def get(self, request):
        try:
            # プラットフォームの確認
            platform = request.query_params.get('platform')
            if platform and platform != 'yahoo':
                return Response({
                    'success': False,
                    'message': f'未対応のプラットフォーム: {platform}'
                }, status=status.HTTP_400_BAD_REQUEST)
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

class ItemDetailView(APIView):
    """
    ヤフオクの商品詳細API
    """
    def get(self, request):
        try:
            service = ScrapingService()
            # Yahooオークションの詳細情報取得
            result = service.get_item_detail(request.query_params)

            return Response({
                'success': True,
                'message': '商品詳細が取得されました',
                'data': result
            })

        except ValueError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
