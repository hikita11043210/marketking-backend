from rest_framework.views import APIView
from api.services.synchronize.ebay import Status
from api.utils.response_helpers import create_success_response, create_error_response

class SynchronizeEbayView(APIView):
    def get(self, request):
        try:
            response = Status(request.user).synchronize()
            return create_success_response(data=response, message="ステータスの同期が完了しました")
        except Exception as e:
            return create_error_response(str(e))
