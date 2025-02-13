from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.ebay_searvices import EbayService

class EbayItemSpecificsView(APIView):
    def get(self, request):
        ebay_item_id = request.query_params.get('ebayItemId')
        if not ebay_item_id:
            return Response(
                {'error': 'ebayItemIdは必須パラメータです'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = request.user
            ebay_service = EbayService(user)
            result = ebay_service.get_item_specifics(ebay_item_id)
            
            if result['success']:
                return Response(result, status=status.HTTP_200_OK)
            return Response(
                {'error': result.get('error', '不明なエラーが発生しました')},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
