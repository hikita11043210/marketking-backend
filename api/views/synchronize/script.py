from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.synchronize.yahoo_auction import YahooAuction
from api.services.synchronize.status import Status
from api.utils.generate_log_file import generate_log_file

class SynchronizeScriptView(APIView):
    def get(self, request):
        try:
            status_response = Status(request.user).synchronize()
            yahoo_auction_response = YahooAuction(request.user).synchronize()
            generate_log_file(yahoo_auction_response, "script/yahoo_auction/response", date=True)
            generate_log_file(status_response, "script/status/response", date=True)
            
            return Response({
                'status': 'success',
                'message': '同期処理が完了しました',
                'data': {
                    'status_response': status_response,
                    'yahoo_auction_response': yahoo_auction_response
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_message = str(e)
            generate_log_file(error_message, "script/error/error", date=True)
            return Response({
                'status': 'error',
                'message': 'エラーが発生しました',
                'error': error_message
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
