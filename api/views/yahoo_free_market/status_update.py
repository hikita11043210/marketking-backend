from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models.yahoo import YahooFreeMarket
from api.serializers import YahooFreeMarketStatusUpdateSerializer
from api.models.master import YahooFreeMarketStatus


class YahooFreeMarketStatusUpdateAPIView(APIView):
    """Yahooフリマのステータス更新API"""
    
    def put(self, request, pk):
        try:
            yahoo_free_market = YahooFreeMarket.objects.get(pk=pk, user=request.user)
        except YahooFreeMarket.DoesNotExist:
            return Response({"detail": "指定されたフリマ情報が見つかりません"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = YahooFreeMarketStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            status_id = serializer.validated_data['status_id']
            try:
                status_obj = YahooFreeMarketStatus.objects.get(pk=status_id)
                yahoo_free_market.status = status_obj
                yahoo_free_market.save()
                return Response({"detail": "ステータスが正常に更新されました"}, status=status.HTTP_200_OK)
            except YahooFreeMarketStatus.DoesNotExist:
                return Response({"detail": "指定されたステータスが存在しません"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 