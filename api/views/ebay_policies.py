from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.services.ebay_searvices import EbayService
from api.utils.throttles import AuctionDetailThrottle
class EbayPoliciesView(APIView):
    """eBayのポリシー情報を取得するView"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuctionDetailThrottle]

    def get(self, request):
        policy_type = request.query_params.get('type', 'all')
        ebay_service = EbayService(request.user)
        
        try:
            if policy_type == 'payment':
                policies = ebay_service.get_payment_policies()
            elif policy_type == 'return':
                policies = ebay_service.get_return_policies()
            elif policy_type == 'fulfillment':
                policies = ebay_service.get_fulfillment_policies()
            else:
                # すべてのポリシーを取得
                policies = {
                    'success': True,
                    'message': 'すべてのポリシーを取得しました',
                    'data': {
                        'payment': ebay_service.get_payment_policies(),
                        'return': ebay_service.get_return_policies(),
                        'fulfillment': ebay_service.get_fulfillment_policies()
                    }
                }
            
            return Response(policies, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

