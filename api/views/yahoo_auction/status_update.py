from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models.yahoo import YahooAuction
from api.serializers import YahooAuctionStatusUpdateSerializer
from api.models.master import YahooAuctionStatus


class YahooAuctionStatusUpdateAPIView(APIView):
    """Yahooオークションのステータス更新API"""
    
    def put(self, request, pk):
        try:
            yahoo_auction = YahooAuction.objects.get(pk=pk, user=request.user)
        except YahooAuction.DoesNotExist:
            return Response({"detail": "指定されたオークション情報が見つかりません"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = YahooAuctionStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            status_id = serializer.validated_data['status_id']
            try:
                status_obj = YahooAuctionStatus.objects.get(pk=status_id)
                yahoo_auction.status = status_obj
                yahoo_auction.save()
                return Response({"detail": "ステータスが正常に更新されました"}, status=status.HTTP_200_OK)
            except YahooAuctionStatus.DoesNotExist:
                return Response({"detail": "指定されたステータスが存在しません"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 