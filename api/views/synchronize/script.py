from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.tasks import sync_yahoo_auction, sync_yahoo_free_market, sync_ebay, send_sync_notification
from celery import chain, group
import logging

logger = logging.getLogger(__name__)

class SynchronizeScriptView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # 同期タスクをグループ化
            sync_tasks = group([
                sync_yahoo_auction.s(),
                sync_yahoo_free_market.s(),
                sync_ebay.s()
            ])

            # 同期タスク完了後にメール送信タスクを実行
            workflow = chain(
                sync_tasks,
                send_sync_notification.s()
            )
            
            # タスクチェーンを実行
            result = workflow.apply_async()
            
            # タスクの結果を待たずに即座にレスポンスを返す
            return Response({
                'status': 'accepted',
                'message': '同期処理を開始しました',
            }, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            logger.error(f"同期処理の開始に失敗しました: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'エラーが発生しました',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
