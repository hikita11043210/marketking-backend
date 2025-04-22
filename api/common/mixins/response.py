from rest_framework import status
from ..response_helpers import (
    success_response, error_response, validation_error_response,
    not_found_response, unauthorized_response, forbidden_response, 
    CustomPagination
)
import logging

logger = logging.getLogger(__name__)

class ResponseMixin:
    """
    DRFビューの拡張用ミックスイン
    一貫性のあるレスポンスフォーマットを提供します
    """
    
    def success_response(self, data=None, message="処理が完了しました", status_code=status.HTTP_200_OK, headers=None):
        """成功レスポンスを返す"""
        return success_response(data, message, status_code, headers)
    
    def error_response(self, exception=None, message=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, errors=None, headers=None):
        """エラーレスポンスを返す"""
        return error_response(exception, message, status_code, errors, headers)
    
    def validation_error_response(self, errors, message="入力内容に誤りがあります", status_code=status.HTTP_400_BAD_REQUEST, headers=None):
        """バリデーションエラーレスポンスを返す"""
        return validation_error_response(errors, message, status_code, headers)
    
    def not_found_response(self, message="リソースが見つかりません", headers=None):
        """Not Foundレスポンスを返す"""
        return not_found_response(message, headers)
    
    def unauthorized_response(self, message="認証が必要です", headers=None):
        """認証エラーレスポンスを返す"""
        return unauthorized_response(message, headers)
    
    def forbidden_response(self, message="権限がありません", headers=None):
        """権限エラーレスポンスを返す"""
        return forbidden_response(message, headers)


class PaginationMixin:
    """
    ページネーション機能を提供するミックスイン
    """
    pagination_class = CustomPagination
    
    def paginate_queryset(self, queryset):
        """
        クエリセットをページネーションする
        """
        if self.paginator is None:
            self.paginator = self.pagination_class()
        return self.paginator.paginate_queryset(queryset, self.request, view=self)
    
    def get_paginated_response(self, data):
        """
        ページネーション付きレスポンスを返す
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data) 