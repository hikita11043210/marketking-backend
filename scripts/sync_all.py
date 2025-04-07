import os
import sys
from pathlib import Path
import requests
import json
from datetime import datetime
import logging
import time

# プロジェクトのルートディレクトリをPYTHONPATHに追加
project_root = str(Path(__file__).resolve().parent.parent)
sys.path.append(project_root)

# Django設定を読み込む
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from api.services.mail.mail import EmailService

logger = logging.getLogger(__name__)

# 設定
API_BASE_URL = "https://market-king-backend-app-a8a6479c97ad.herokuapp.com/api/v1"
# API_BASE_URL = "http://localhost:8000/api/v1"
RECIPIENT_EMAILS = ['th.osigoto0719@gmail.com']
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def get_access_token():
    """ログインAPIを呼び出してアクセストークンを取得"""
    try:
        login_url = f'{API_BASE_URL}/auth/login/'
        login_data = {
            'username': 'anakin0512',
            'password': 'Popo3gou!'
        }
        
        response = requests.post(login_url, json=login_data)
        response.raise_for_status()
        return response.json()['accessToken']
    except Exception as e:
        logger.error(f"ログインに失敗しました: {str(e)}")
        raise

def call_sync_api(access_token):
    """同期APIを呼び出す"""
    sync_url = f'{API_BASE_URL}/synchronize/script/'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    for retry in range(MAX_RETRIES):
        try:
            response = requests.get(
                sync_url,
                headers=headers,
                timeout=600  # 10分のタイムアウト
            )
            response.raise_for_status()
            response_data = response.json()
            
            logger.info('同期処理が完了しました')
            send_notification(create_email_body(response_data))
            return True
            
        except requests.exceptions.Timeout:
            logger.error(f'タイムアウトが発生しました (試行 {retry + 1}/{MAX_RETRIES})')
            if retry < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return False
            
        except requests.exceptions.RequestException as e:
            logger.error(f'同期APIエラー (試行 {retry + 1}/{MAX_RETRIES}): {str(e)}')
            if hasattr(e.response, 'text'):
                logger.error(f'エラー詳細: {e.response.text}')
            if retry < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return False

def send_notification(message):
    """メール通知を送信する"""
    try:
        email_service = EmailService()
        recipient_emails = RECIPIENT_EMAILS
        subject = 'Market King 同期更新'
        result = email_service.send_email_to_multiple_users(recipient_emails, subject, message)
        if result['success']:
            logger.info(f'メール通知が送信されました: {result["success"]}')
        if result['failed']:
            logger.error(f'メール通知の送信に失敗しました: {result["failed"]}')
    except Exception as e:
        logger.error(f'メール送信エラー: {str(e)}')

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

def should_run():
    """実行時間のチェック"""
    current_hour = datetime.now().hour
    target_hours = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    return current_hour in target_hours

def run_sync():
    """同期処理を実行"""
    try:
        if not should_run():
            logger.info("同期実行時間ではありません")
            return

        logger.info("同期処理を開始します...")
        
        # JWTトークンを取得
        access_token = get_access_token()
        
        # 同期APIを呼び出し
        success = call_sync_api(access_token)
        
        if success:
            logger.info("同期処理が正常に完了しました")
        else:
            logger.error("同期処理が失敗しました")
            
    except Exception as e:
        logger.error(f"同期処理中にエラーが発生しました: {str(e)}")
        # エラー時もメール通知
        error_body = f"同期処理でエラーが発生しました。\nエラー: {str(e)}"
        send_notification(error_body)

if __name__ == '__main__':
    run_sync() 