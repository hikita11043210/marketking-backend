from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.models import Sales
from api.serializers.sales import SalesSerializer
from api.mixins import CustomListCreateMixin, CustomDetailMixin


class SaleListCreateAPIView(CustomListCreateMixin, generics.ListCreateAPIView):
    """売上データの一覧取得・新規作成API"""
    queryset = Sales.objects.filter(is_deleted=False)
    serializer_class = SalesSerializer
    permission_classes = [IsAuthenticated]


class SaleDetailAPIView(CustomDetailMixin, generics.RetrieveUpdateDestroyAPIView):
    """売上データの詳細取得・更新・削除API"""
    queryset = Sales.objects.filter(is_deleted=False)
    serializer_class = SalesSerializer
    permission_classes = [IsAuthenticated] 