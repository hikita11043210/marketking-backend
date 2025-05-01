from celery import shared_task, group
from api.services.synchronize.yahoo_auction import SynchronizeYahooAuction
from api.services.synchronize.ebay import Status as EbayStatus
from api.services.synchronize.yahoo_free_market import SynchronizeYahooFreeMarket
from api.services.mail.mail import EmailService
from api.utils.email_body import create_email_body
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@shared_task
def sync_yahoo_auction():
    try:
        yahoo_auction = SynchronizeYahooAuction()
        result = yahoo_auction.synchronize()
        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f"Yahoo Auction同期中にエラーが発生しました: {str(e)}")
        return {'status': 'error', 'error': str(e)}

@shared_task
def sync_yahoo_free_market():
    try:
        yahoo_free_market = SynchronizeYahooFreeMarket()
        result = yahoo_free_market.synchronize()
        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f"Yahoo Free Market同期中にエラーが発生しました: {str(e)}")
        return {'status': 'error', 'error': str(e)}

@shared_task
def sync_ebay():
    try:
        ebay = EbayStatus()
        result = ebay.synchronize()
        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f"eBay同期中にエラーが発生しました: {str(e)}")
        return {'status': 'error', 'error': str(e)}

# メール送信用の新しいタスクを追加
@shared_task
def send_sync_notification(results, start_time=None):
    """
    同期処理の結果をメールで通知するタスク
    results: 各同期タスクの結果のリスト
    start_time: 同期処理の開始時刻
    """
    try:
        from datetime import datetime, timedelta

        # 現在時刻を終了時刻として記録（UTC）
        utc_end_time = datetime.now()
        
        # UTC時間を日本時間（JST）に変換（+9時間）
        jst_end_time = (utc_end_time + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
        
        # 開始時刻も日本時間に変換
        jst_start_time = None
        if start_time:
            try:
                # 文字列から日時オブジェクトに変換
                utc_start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                # JST（+9時間）に変換
                jst_start_time = (utc_start_time + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                # 変換できない場合はそのまま使用
                jst_start_time = start_time
        
        # 結果データの整形
        response_data = {
            'yahoo_auction': results[0].get('data') if results[0].get('status') == 'success' else {'error': results[0].get('error')},
            'yahoo_free_market': results[1].get('data') if results[1].get('status') == 'success' else {'error': results[1].get('error')},
            'ebay': results[2].get('data') if results[2].get('status') == 'success' else {'error': results[2].get('error')},
            'start_time': jst_start_time,
            'end_time': jst_end_time
        }

        # メール本文の作成と送信
        email_service = EmailService()
        recipient_emails = ['th.osigoto0719@gmail.com']
        subject = 'Market King 同期更新'
        message = create_email_body(response_data)
        
        result = email_service.send_email_to_multiple_users(recipient_emails, subject, message)
        
        if result['success']:
            logger.info(f'メール通知が送信されました: {result["success"]}')
        if result['failed']:
            logger.error(f'メール通知の送信に失敗しました: {result["failed"]}')
            
    except Exception as e:
        logger.error(f'メール送信エラー: {str(e)}')
        raise

@shared_task
def sync_yahoo_free_market_manual(user_id):
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)
        
        yahoo_free_market = SynchronizeYahooFreeMarket(user)
        result = yahoo_free_market.synchronize()

    #     # WebSocketを通じて結果を送信
    #     channel_layer = get_channel_layer()
    #     async_to_sync(channel_layer.group_send)(
    #         f"user_{user_id}",
    #         {
    #             "type": "sync.completed",
    #             "message": {
    #                 "status": "success",
    #                 "data": result
    #             }
    #         }
    #     )
        
    #     return result
    # except Exception as e:
    #     # エラー時もWebSocketで通知
    #     channel_layer = get_channel_layer()
    #     async_to_sync(channel_layer.group_send)(
    #         f"user_{user_id}",
    #         {
    #             "type": "sync.error",
    #             "message": {
    #                 "status": "error",
    #                 "error": str(e)
    #             }
    #         }
    #     )
    #     raise

        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f"Yahoo Free Market同期中にエラーが発生しました: {str(e)}")
        return {'status': 'error', 'error': str(e)}

@shared_task
def sync_yahoo_auction_manual(user_id):
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.get(id=user_id)

        yahoo_auction = SynchronizeYahooAuction(user)
        result = yahoo_auction.synchronize()
        return {'status': 'success', 'data': result}
    except Exception as e:
        logger.error(f"Yahoo Auction同期中にエラーが発生しました: {str(e)}")
        return {'status': 'error', 'error': str(e)}
