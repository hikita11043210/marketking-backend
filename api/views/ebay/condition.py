from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.services.ebay.marketplace import Marketplace
from api.utils.throttles import AuctionDetailThrottle
from api.utils.response_helpers import create_success_response, create_error_response

class EbayConditionView(APIView):
    """eBayのコンディション情報を取得するView"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuctionDetailThrottle]

    def get(self, request):
        category_id = request.query_params.get('categoryId')
        ebay_service_marketplace = Marketplace(request.user)
        
        try:
            conditions = ebay_service_marketplace.get_category_conditions(category_id)
            return create_success_response(
                data=conditions,
                message='カテゴリのコンディション情報を取得しました'
            )
        except Exception as e:
            return create_error_response(e)

