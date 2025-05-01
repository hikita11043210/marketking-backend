from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.models import Purchase
from api.serializers.purchases import PurchasesSerializer
from api.mixins import CustomListCreateMixin, CustomDetailMixin


class PurchaseListCreateAPIView(CustomListCreateMixin, generics.ListCreateAPIView):
    """仕入れデータの一覧取得・新規作成API"""
    queryset = Purchase.objects.filter(is_deleted=False)
    serializer_class = PurchasesSerializer
    permission_classes = [IsAuthenticated]


class PurchaseDetailAPIView(CustomDetailMixin, generics.RetrieveUpdateDestroyAPIView):
    """仕入れデータの詳細取得・更新・削除API"""
    queryset = Purchase.objects.filter(is_deleted=False)
    serializer_class = PurchasesSerializer
    permission_classes = [IsAuthenticated] 