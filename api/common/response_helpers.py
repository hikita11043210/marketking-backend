from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
import logging
import traceback
from django.conf import settings

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    """
    カスタムページネーションクラス
    page_sizeはデフォルトで10に設定されています
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        共通フォーマットのページネーションレスポンスを返す
        """
        return Response({
            'success': True,
            'message': '処理が完了しました',
            'data': data,
            'pagination': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_size': self.page_size,
            }
        })


def success_response(data=None, message="処理が完了しました", status_code=status.HTTP_200_OK, headers=None):
    """
    成功時のレスポンスを生成する
    Args:
        data: レスポンスデータ
        message: 成功メッセージ
        status_code: HTTPステータスコード
        headers: カスタムヘッダー
    Returns:
        Response: DRFのレスポンスオブジェクト
    """
    response_data = {
        'success': True,
        'message': message,
        'data': data
    }
    
    return Response(response_data, status=status_code, headers=headers)


def error_response(exception=None, message=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, errors=None, headers=None):
    """
    エラー時のレスポンスを生成する
    Args:
        exception: 発生した例外
        message: エラーメッセージ（Noneの場合は例外のメッセージを使用）
        status_code: HTTPステータスコード
        errors: 詳細エラーリスト（フィールドごとのバリデーションエラーなど）
        headers: カスタムヘッダー
    Returns:
        Response: DRFのレスポンスオブジェクト
    """
    error_message = message
    
    if error_message is None and exception is not None:
        error_message = str(exception)
    
    # エラーログを出力
    if exception is not None:
        logger.error(f"Error occurred: {str(exception)}")
        if settings.DEBUG:
            logger.error(traceback.format_exc())
    
    response_data = {
        'success': False,
        'message': error_message,
        'data': None
    }
    
    if errors is not None:
        response_data['errors'] = errors
    
    return Response(response_data, status=status_code, headers=headers)


def validation_error_response(errors, message="入力内容に誤りがあります", status_code=status.HTTP_400_BAD_REQUEST, headers=None):
    """
    バリデーションエラー時のレスポンスを生成する
    Args:
        errors: バリデーションエラーのディクショナリ
        message: エラーメッセージ
        status_code: HTTPステータスコード
        headers: カスタムヘッダー
    Returns:
        Response: DRFのレスポンスオブジェクト
    """
    return Response(
        {
            'success': False,
            'message': message,
            'data': None,
            'errors': errors
        },
        status=status_code,
        headers=headers
    )


def not_found_response(message="リソースが見つかりません", headers=None):
    """
    リソースが見つからない場合のレスポンスを生成する
    Args:
        message: エラーメッセージ
        headers: カスタムヘッダー
    Returns:
        Response: DRFのレスポンスオブジェクト
    """
    return Response(
        {
            'success': False,
            'message': message,
            'data': None
        },
        status=status.HTTP_404_NOT_FOUND,
        headers=headers
    )


def unauthorized_response(message="認証が必要です", headers=None):
    """
    認証が必要な場合のレスポンスを生成する
    Args:
        message: エラーメッセージ
        headers: カスタムヘッダー
    Returns:
        Response: DRFのレスポンスオブジェクト
    """
    return Response(
        {
            'success': False,
            'message': message,
            'data': None
        },
        status=status.HTTP_401_UNAUTHORIZED,
        headers=headers
    )


def forbidden_response(message="権限がありません", headers=None):
    """
    権限がない場合のレスポンスを生成する
    Args:
        message: エラーメッセージ
        headers: カスタムヘッダー
    Returns:
        Response: DRFのレスポンスオブジェクト
    """
    return Response(
        {
            'success': False,
            'message': message,
            'data': None
        },
        status=status.HTTP_403_FORBIDDEN,
        headers=headers
    )


# 既存のメソッド名との後方互換性を維持
create_success_response = success_response
create_error_response = error_response 