from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.scraping.yahoo_auction import YahooAuctionService
from ..services.currency import CurrencyService
import logging

logger = logging.getLogger(__name__)    

class YahooAuctionItemSearchView(APIView):
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
            service = YahooAuctionService()
            result = service.search_items(request.query_params)
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

class YahooAuctionCategorySearchView(APIView):
    """
    ヤフオクのカテゴリ検索API
    """
    def get(self, request):
        try:
            service = YahooAuctionService()
            result = service.search_categories(request.query_params)
            return Response({
                'success': True,
                'message': 'カテゴリ検索が完了しました',
                'data': result
            })
        except ValueError as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"カテゴリ検索でエラーが発生: {str(e)}")
            return Response({
                'success': False,
                'message': 'カテゴリ検索に失敗しました'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
class YahooAuctionDetailView(APIView):
    """
    ヤフオクの商品詳細API
    """
    def get(self, request):
        try:
            service = YahooAuctionService()
            # Yahooオークションの詳細情報取得
            result = service.get_item_detail(request.query_params)

            # # 為替レートの取得
            # currency_service = CurrencyService()
            # result['data']['current_price_in_tax'] = currency_service.convert_currency(result['data']['current_price'], 'JPY', 'USD')
            # result['data']['buy_now_price_in_tax'] = currency_service.convert_currency(result['data']['buy_now_price'], 'JPY', 'USD')

            # # 利率をかけた価格を作成
            # result['data']['current_price_in_tax'] = currency_service.convert_currency(result['data']['current_price'], 'JPY', 'USD')

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
