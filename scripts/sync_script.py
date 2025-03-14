import requests
import json
import os
from datetime import datetime

# 設定
API_BASE_URL = os.getenv('BACKEND_URL') + "/api/v1"  # DjangoのAPIのベースURL
USERNAME = 'toshiki'  # ユーザー名
PASSWORD = 'popo3gou'  # パスワード

def get_jwt_token():
    """JWTトークンを取得する"""
    login_url = f'{API_BASE_URL}/auth/login/'
    
    try:
        response = requests.post(
            login_url,
            json={
                'username': USERNAME,
                'password': PASSWORD
            }
        )
        response.raise_for_status()
        return response.json()['accessToken']
    except requests.exceptions.RequestException as e:
        print(f'ログインエラー: {str(e)}')
        if hasattr(e.response, 'text'):
            print(f'エラー詳細: {e.response.text}')
        return None

def call_sync_api(access_token):
    """同期APIを呼び出す"""
    sync_url = f'{API_BASE_URL}/synchronize/script/'
    
    try:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(sync_url, headers=headers)
        response.raise_for_status()
        
        response_data = response.json()
        print(f'ステータス: {response_data["status"]}')
        print(f'メッセージ: {response_data["message"]}')
        if response_data["status"] == "error":
            print(f'エラー詳細: {response_data["error"]}')
        
        return True
    except requests.exceptions.RequestException as e:
        print(f'同期APIエラー: {str(e)}')
        if hasattr(e.response, 'text'):
            print(f'エラー詳細: {e.response.text}')
        return False

def main():
    print('同期処理を開始します...')
    
    # JWTトークンを取得
    access_token = get_jwt_token()
    if not access_token:
        print('JWTトークンの取得に失敗しました')
        return False
    
    print('JWTトークンの取得に成功しました')
    # 同期APIを呼び出し
    success = call_sync_api(access_token)
    return success

if __name__ == '__main__':
    main() 