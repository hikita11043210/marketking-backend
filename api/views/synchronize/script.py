from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.synchronize.yahoo_auction import SynchronizeYahooAuction
from api.services.synchronize.ebay import Status
from api.services.synchronize.yahoo_free_market import SynchronizeYahooFreeMarket
import asyncio
from asgiref.sync import sync_to_async
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class SynchronizeScriptView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @sync_to_async
    def _run_status_sync(self, user):
        status_sync = Status(user)
        return status_sync.synchronize()

    @sync_to_async
    def _run_yahoo_auction_sync(self, user):
        yahoo_auction_sync = SynchronizeYahooAuction(user)
        return yahoo_auction_sync.synchronize()

    @sync_to_async
    def _run_yahoo_free_market_sync(self, user):
        yahoo_free_market_sync = SynchronizeYahooFreeMarket(user)
        return yahoo_free_market_sync.synchronize()

    async def get(self, request):
        try:
            # 各同期処理を非同期で実行
            status_response = await self._run_status_sync(request.user)
            yahoo_auction_response = await self._run_yahoo_auction_sync(request.user)
            yahoo_free_market_response = await self._run_yahoo_free_market_sync(request.user)
            
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
