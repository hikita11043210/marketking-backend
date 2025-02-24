from rest_framework.views import APIView
from api.services.synchronize.yahoo_auction import YahooAuction
from api.utils.response_helpers import create_success_response, create_error_response

class SynchronizeYahooAuctionView(APIView):
    def get(self, request):
        try:
            response = YahooAuction(request.user).synchronize()
            return create_success_response(message="ステータスの同期が完了しました")
        except Exception as e:
            return create_error_response(str(e))