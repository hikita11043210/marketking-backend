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
    
    try:
        response = requests.get(
            sync_url,
            headers=headers,
            timeout=600
        )
        response.raise_for_status()
        
        if response.status_code == 202:  # Accepted
            return True
            
    except requests.exceptions.RequestException as e:
        logger.error(f'同期APIエラー: {str(e)}')
        if hasattr(e.response, 'text'):
            logger.error(f'エラー詳細: {e.response.text}')
        return False

def should_run():
    """実行時間のチェック"""
    current_hour = datetime.now().hour
    target_hours = [0, 3, 6, 9, 12, 15, 18]
    return current_hour in target_hours

def run_sync():
    """同期処理を実行"""
    try:
        if not should_run():
            logger.info("同期実行時間ではありません")
            return

        logger.info("JWTトークンを取得します...")

        # JWTトークンを取得
        access_token = get_access_token()

        logger.info("同期APIを呼び出します...")

        # 同期APIを呼び出し
        success = call_sync_api(access_token)
        
        if success:
            logger.info("同期処理を開始しました")
        else:
            logger.error("同期処理が失敗しました")
            
    except Exception as e:
        logger.error(f"同期処理中にエラーが発生しました: {str(e)}")
        # エラー時もメール通知
        error_body = f"同期処理でエラーが発生しました。\nエラー: {str(e)}"
        email_service = EmailService()
        email_service.send_email_to_multiple_users(RECIPIENT_EMAILS, 'Market King 同期更新エラー', error_body)

if __name__ == '__main__':
    run_sync() 