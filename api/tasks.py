from celery import shared_task, group
from api.services.synchronize.yahoo_auction import SynchronizeYahooAuction
from api.services.synchronize.ebay import Status as EbayStatus
from api.services.synchronize.yahoo_free_market import SynchronizeYahooFreeMarket
from api.services.mail.mail import EmailService
from api.views.synchronize.script import create_email_body
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

def create_email_body(response_data):
    """同期処理の結果からメール本文を作成する"""
    body = "Market King 同期処理結果のお知らせ\n"
    body += "=" * 50 + "\n\n"

    # Yahoo Auction
    yahoo_auction_data = response_data.get('yahoo_auction', {})
    if yahoo_auction_data:
        body += "【Yahoo!オークション商品同期】\n"
        if isinstance(yahoo_auction_data, dict) and 'error' not in yahoo_auction_data:
            body += f"処理開始時刻: {yahoo_auction_data.get('synchronize_start_time', '-')}\n"
            body += f"処理終了時刻: {yahoo_auction_data.get('synchronize_end_time', '-')}\n"
            body += f"対象商品数: {yahoo_auction_data.get('synchronize_target_item', 0)}\n"
            body += f"ステータス変更商品数: {yahoo_auction_data.get('count_change_status_item', 0)}\n\n"
        else:
            body += f"エラーが発生しました: {yahoo_auction_data.get('error', '不明なエラー')}\n\n"

    # Yahoo Free Market
    yahoo_free_market_data = response_data.get('yahoo_free_market', {})
    if yahoo_free_market_data:
        body += "【Yahoo!フリマ商品同期】\n"
        if isinstance(yahoo_free_market_data, dict) and 'error' not in yahoo_free_market_data:
            body += f"処理開始時刻: {yahoo_free_market_data.get('synchronize_start_time', '-')}\n"
            body += f"処理終了時刻: {yahoo_free_market_data.get('synchronize_end_time', '-')}\n"
            body += f"対象商品数: {yahoo_free_market_data.get('synchronize_target_item', 0)}\n"
            body += f"ステータス変更商品数: {yahoo_free_market_data.get('count_change_status_item', 0)}\n\n"
        else:
            body += f"エラーが発生しました: {yahoo_free_market_data.get('error', '不明なエラー')}\n\n"

    # eBay
    ebay_data = response_data.get('ebay', {})
    if ebay_data:
        body += "【eBay商品同期】\n"
        if isinstance(ebay_data, dict) and 'error' not in ebay_data:
            body += f"処理開始時刻: {ebay_data.get('synchronize_start_time', '-')}\n"
            body += f"処理終了時刻: {ebay_data.get('synchronize_end_time', '-')}\n"
            body += f"対象商品数: {ebay_data.get('synchronize_target_item', 0)}\n"
            body += f"ステータス変更商品数: {ebay_data.get('count_change_status_item', 0)}\n\n"
        else:
            body += f"エラーが発生しました: {ebay_data.get('error', '不明なエラー')}\n\n"

    body += "=" * 50 + "\n"
    body += "※このメールは自動送信されています。"
    
    return body