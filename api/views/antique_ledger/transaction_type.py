from rest_framework import generics, permissions
from api.models import TransactionType
from api.serializers import TransactionTypeSerializer


class TransactionTypeListAPIView(generics.ListAPIView):
    """取引区分マスタを取得するAPI"""
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
    permission_classes = [permissions.IsAuthenticated] 