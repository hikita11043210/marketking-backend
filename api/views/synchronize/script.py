from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.synchronize.yahoo_auction import SynchronizeYahooAuction
from api.services.synchronize.ebay import Status
from api.services.synchronize.yahoo_free_market import SynchronizeYahooFreeMarket
import asyncio

class SynchronizeScriptView(APIView):
    async def get(self, request):
        try:
            # 各同期処理を実行
            status_sync = Status(request.user)
            yahoo_auction_sync = SynchronizeYahooAuction(request.user)
            yahoo_free_market_sync = SynchronizeYahooFreeMarket(request.user)

            # 非同期で実行
            status_response = status_sync.synchronize()  # これは同期のまま
            yahoo_auction_response = yahoo_auction_sync.synchronize()  # これは同期のまま
            yahoo_free_market_response = await yahoo_free_market_sync.synchronize()  # これを非同期に
            
            return Response({
                'status': 'success',
                'message': '同期処理が完了しました',
                'data': {
                    'status_response': status_response,
                    'yahoo_auction_response': yahoo_auction_response,
                    'yahoo_free_market_response': yahoo_free_market_response
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_message = str(e)
            return Response({
                'status': 'error',
                'message': 'エラーが発生しました',
                'error': error_message
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
