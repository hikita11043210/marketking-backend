from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import Expense
from api.serializers.expenses import ExpensesSerializer


class ExpenseListCreateAPIView(generics.ListCreateAPIView):
    """経費データの一覧取得・新規作成API"""
    queryset = Expense.objects.filter(is_deleted=False)
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ExpenseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """経費データの詳細取得・更新・削除API"""
    queryset = Expense.objects.filter(is_deleted=False)
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT) 