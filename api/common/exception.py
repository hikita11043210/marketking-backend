from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied, AuthenticationFailed
from rest_framework.views import exception_handler
from .response_helpers import (
    error_response, validation_error_response,
    not_found_response, unauthorized_response, forbidden_response, 
)
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    DRFのデフォルト例外ハンドラを拡張して、共通フォーマットのレスポンスを返す
    """
    # デフォルトのハンドラを呼び出し、レスポンスを取得
    response = exception_handler(exc, context)
    
    # レスポンスがない場合は、カスタムレスポンスを生成
    if response is None:
        if isinstance(exc, Exception):
            return error_response(exception=exc)
        return None
    
    # 特定の例外タイプに応じたカスタムレスポンスを生成
    if isinstance(exc, ValidationError):
        return validation_error_response(errors=response.data)
    
    if isinstance(exc, NotFound):
        return not_found_response(message=str(exc))
    
    if isinstance(exc, AuthenticationFailed):
        return unauthorized_response(message=str(exc))
    
    if isinstance(exc, PermissionDenied):
        return forbidden_response(message=str(exc))
    
    # その他の例外の場合は、一般的なエラーレスポンスを生成
    return error_response(
        message=str(exc),
        status_code=response.status_code
    )
