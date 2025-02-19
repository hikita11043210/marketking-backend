from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def create_success_response(data=None, message="処理が完了しました", status_code=status.HTTP_200_OK):
    """
    成功時のレスポンスを生成する
    Args:
        data: レスポンスデータ
        message: 成功メッセージ
        status_code: HTTPステータスコード
    Returns:
        Response: DRFのレスポンスオブジェクト
    """
    return Response(
        {
            'success': True,
            'message': message,
            'data': data
        },
        status=status_code
    )

def create_error_response(e, message=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    """
    エラー時のレスポンスを生成する
    Args:
        e: 発生した例外
        message: エラーメッセージ（Noneの場合は例外のメッセージを使用）
        status_code: HTTPステータスコード
    Returns:
        Response: DRFのレスポンスオブジェクト
    """
    error_message = message if message is not None else str(e)
    logger.error(f"Error occurred: {str(e)}")
    
    return Response(
        {
            'success': False,
            'message': error_message,
            'data': None
        },
        status=status_code
    ) 