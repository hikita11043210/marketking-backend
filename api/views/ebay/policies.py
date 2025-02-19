from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.services.ebay.policy import Policy
from api.utils.throttles import AuctionDetailThrottle
from api.utils.response_helpers import create_success_response, create_error_response

class EbayPoliciesView(APIView):
    """eBayのポリシー情報を取得するView"""
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuctionDetailThrottle]

    def get(self, request):
        policy_type = request.query_params.get('type', 'all')
        ebay_service_policy = Policy(request.user)
        
        try:
            if policy_type == 'payment':
                policies = ebay_service_policy.get_payment_policies()
            elif policy_type == 'return':
                policies = ebay_service_policy.get_return_policies()
            elif policy_type == 'fulfillment':
                policies = ebay_service_policy.get_fulfillment_policies()
            else:
                # すべてのポリシーを取得
                policies = {
                    'payment': ebay_service_policy.get_payment_policies(),
                    'return': ebay_service_policy.get_return_policies(),
                    'fulfillment': ebay_service_policy.get_fulfillment_policies()
                }
                return create_success_response(
                    data=policies,
                    message='すべてのポリシーを取得しました'
                )
            
            return create_success_response(
                data=policies.get('data'),
                message=policies.get('message', 'ポリシー情報を取得しました')
            )
            
        except Exception as e:
            return create_error_response(e)

