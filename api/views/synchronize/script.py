from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.synchronize.yahoo_auction import SynchronizeYahooAuction
from api.services.synchronize.ebay import Status
from api.services.synchronize.yahoo_free_market import SynchronizeYahooFreeMarket

class SynchronizeScriptView(APIView):
    def get(self, request):
        try:
            status_response = Status(request.user).synchronize()
            yahoo_auction_response = SynchronizeYahooAuction(request.user).synchronize()
            yahoo_free_market_response = SynchronizeYahooFreeMarket(request.user).synchronize()
            
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
