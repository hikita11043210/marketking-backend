from rest_framework.response import Response
from rest_framework import status

class CustomListCreateMixin:
    """リスト取得・作成の共通処理ミックスイン"""
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(insert_user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
    def perform_create(self, serializer):
        serializer.save(
            insert_user=self.request.user,
            update_user=self.request.user
        )


class CustomDetailMixin:
    """詳細・更新・削除の共通処理ミックスイン"""
    
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
    
    def perform_update(self, serializer):
        serializer.save(update_user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT) 