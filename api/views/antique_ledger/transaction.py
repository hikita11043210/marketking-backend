from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Transaction
from api.serializers import TransactionSerializer
from django.utils import timezone


class TransactionListCreateAPIView(generics.ListCreateAPIView):
    """古物台帳の一覧取得と新規登録API"""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_date', 'transaction_type', 'management_code']
    search_fields = ['product_name']
    ordering_fields = ['transaction_date', 'created_at', 'updated_at']
    ordering = ['-transaction_date']

    def get_queryset(self):
        """論理削除されていないレコードのみ取得"""
        return Transaction.objects.filter(is_deleted=False)


class TransactionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """古物台帳の詳細取得、更新、削除API"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """論理削除を行う"""
        instance = self.get_object()
        instance.is_deleted = True
        instance.updated_by = request.user.username
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT) 