from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from api.models import Expense
from api.serializers.expenses import ExpensesSerializer
from api.mixins import CustomListCreateMixin, CustomDetailMixin


class ExpenseListCreateAPIView(CustomListCreateMixin, generics.ListCreateAPIView):
    """経費データの一覧取得・新規作成API"""
    queryset = Expense.objects.filter(is_deleted=False)
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]


class ExpenseDetailAPIView(CustomDetailMixin, generics.RetrieveUpdateDestroyAPIView):
    """経費データの詳細取得・更新・削除API"""
    queryset = Expense.objects.filter(is_deleted=False)
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated] 