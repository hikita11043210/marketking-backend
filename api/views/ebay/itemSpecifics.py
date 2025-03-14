from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.ebay.trading import Trading
from api.services.ebay.category import Category

class EbayItemSpecificsView(APIView):
    def get(self, request):
        ebay_item_id = request.query_params.get('ebayItemId')
        if not ebay_item_id:
            return Response(
                {
                    'success': False,
                    'message': 'ebayItemIdは必須パラメータです'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = request.user
            ebay_service_trading = Trading(user)
            ebay_service_category = Category(user)
            category_tree_id = ebay_service_category.get_categories_tree_id()
            result = ebay_service_trading.get_item_specifics(ebay_item_id, category_tree_id)
            
            return Response(result, status=status.HTTP_200_OK if result['success'] else status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
