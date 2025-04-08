from celery import shared_task, group
from api.services.synchronize.yahoo_auction import SynchronizeYahooAuction
from api.services.synchronize.ebay import Status as EbayStatus
from api.services.synchronize.yahoo_free_market import SynchronizeYahooFreeMarket
from api.services.mail.mail import EmailService
from api.utils.email_body import create_email_body
import logging

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
def send_sync_notification(results):
    """
    同期処理の結果をメールで通知するタスク
    results: 各同期タスクの結果のリスト
    """
    try:
        # 結果データの整形
        response_data = {
            'yahoo_auction': results[0].get('data') if results[0].get('status') == 'success' else {'error': results[0].get('error')},
            'yahoo_free_market': results[1].get('data') if results[1].get('status') == 'success' else {'error': results[1].get('error')},
            'ebay': results[2].get('data') if results[2].get('status') == 'success' else {'error': results[2].get('error')}
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
