import requests
import json
from datetime import datetime
from api.services.mail.mail import EmailService
import time

# 設定
API_BASE_URL = "https://market-king-backend-app-a8a6479c97ad.herokuapp.com/api/v1"
USERNAME = 'anakin0512'
PASSWORD = 'Popo3gou!'
RECIPIENT_EMAILS = ['th.osigoto0719@gmail.com']
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def get_jwt_token():
    """JWTトークンを取得する"""
    login_url = f'{API_BASE_URL}/auth/login/'
    
    for retry in range(MAX_RETRIES):
        try:
            response = requests.post(
                login_url,
                json={
                    'username': USERNAME,
                    'password': PASSWORD
                },
                timeout=30  # Herokuのタイムアウトに合わせる
            )
            response.raise_for_status()
            return response.json()['accessToken']
        except requests.exceptions.RequestException as e:
            print(f'ログインエラー (試行 {retry + 1}/{MAX_RETRIES}): {str(e)}')
            if retry < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return None

def call_sync_api(access_token):
    """同期APIを呼び出す"""
    sync_url = f'{API_BASE_URL}/synchronize/script/'
    
    for retry in range(MAX_RETRIES):
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            response = requests.get(
                sync_url, 
                headers=headers,
                timeout=120  # 長めのタイムアウトを設定
            )
            response.raise_for_status()
            response_data = response.json()

            if response_data["status"] == "success":
                print(f'同期処理が完了しました')
                send_notification(create_email_body(response_data))
            else:
                print(f'同期処理でエラーが発生しました')
                print(f'エラー詳細: {response_data.get("error", "不明なエラー")}')
            
            return True

        except requests.exceptions.Timeout:
            print(f'タイムアウトが発生しました (試行 {retry + 1}/{MAX_RETRIES})')
            if retry < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return False

        except requests.exceptions.RequestException as e:
            print(f'同期APIエラー (試行 {retry + 1}/{MAX_RETRIES}): {str(e)}')
            if hasattr(e.response, 'text'):
                print(f'エラー詳細: {e.response.text}')
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
            print(f'メール通知が送信されました: {result["success"]}')
        if result['failed']:
            print(f'メール通知の送信に失敗しました: {result["failed"]}')
    except Exception as e:
        print(f'メール送信エラー: {str(e)}')

def create_email_body(response_data):
    """同期処理の結果からメール本文を作成する"""
    if response_data["status"] != "success":
        return f"同期処理でエラーが発生しました。\nエラー: {response_data.get('error', '不明なエラー')}"

    data = response_data["data"]
    
    # メール本文の作成
    body = "Market King 同期処理結果のお知らせ\n"
    body += "=" * 50 + "\n\n"

    # eBayのステータス同期結果
    if "status_response" in data:
        status_data = data["status_response"]
        body += "【eBay商品ステータス同期】\n"
        
        # status_dataが文字列の場合（エラー発生時）
        if isinstance(status_data, str):
            body += f"エラーが発生しました: {status_data}\n\n"
        else:
            try:
                body += f"処理開始時刻: {status_data['synchronize_start_time']}\n"
                body += f"処理終了時刻: {status_data['synchronize_end_time']}\n"
                body += f"対象商品数: {status_data['synchronize_target_item']}\n"
                body += f"アクティブ商品数: {status_data['count_active_item']}\n"
                body += f"売れた商品数: {status_data['count_sold_out_item']}\n"
                body += f"ステータス変更商品数: {status_data['count_change_status_item']}\n\n"

                if status_data.get('updated_items'):
                    body += "ステータス変更された商品:\n"
                    for item in status_data['updated_items']:
                        body += f"- SKU: {item['sku']}\n"
                        body += f"  旧ステータス: {item['old_status']} → 新ステータス: {item['new_status']}\n"
                        if item.get('url'):
                            body += f"  URL: {item['url']}\n"
                    body += "\n"
            except KeyError as e:
                body += f"データの取得に失敗しました: {str(e)}\n\n"

    # Yahooオークションの同期結果
    if "yahoo_auction_response" in data:
        yahoo_auction_data = data["yahoo_auction_response"]
        body += "【Yahoo!オークション商品同期】\n"
        
        # yahoo_auction_dataが文字列の場合（エラー発生時）
        if isinstance(yahoo_auction_data, str):
            body += f"エラーが発生しました: {yahoo_auction_data}\n\n"
        else:
            try:
                body += f"処理開始時刻: {yahoo_auction_data['synchronize_start_time']}\n"
                body += f"処理終了時刻: {yahoo_auction_data['synchronize_end_time']}\n"
                body += f"対象商品数: {yahoo_auction_data['synchronize_target_item']}\n"
                # body += f"アクティブ商品数: {yahoo_auction_data['count_active_item']}\n"
                # body += f"売切れ商品数: {yahoo_auction_data['count_sold_out_item']}\n"
                body += f"ステータス変更商品数: {yahoo_auction_data['count_change_status_item']}\n\n"

                if yahoo_auction_data.get('updated_items'):
                    body += "ステータス変更された商品:\n"
                    for item in yahoo_auction_data['updated_items']:
                        body += f"- 商品ID: {item['unique_id']}\n"
                        body += f"  旧ステータス: {item['old_status']} → 新ステータス: {item['new_status']}\n"
                    body += "\n"
            except KeyError as e:
                body += f"データの取得に失敗しました: {str(e)}\n\n"

    # Yahooフリマの同期結果
    if "yahoo_free_market_response" in data:
        yahoo_data = data["yahoo_free_market_response"]
        body += "【Yahoo!フリマ商品同期】\n"
        
        # yahoo_dataが文字列の場合（エラー発生時）
        if isinstance(yahoo_data, str):
            body += f"エラーが発生しました: {yahoo_data}\n\n"
        else:
            try:
                body += f"処理開始時刻: {yahoo_data['synchronize_start_time']}\n"
                body += f"処理終了時刻: {yahoo_data['synchronize_end_time']}\n"
                body += f"対象商品数: {yahoo_data['synchronize_target_item']}\n"
                # body += f"アクティブ商品数: {yahoo_data['count_active_item']}\n"
                # body += f"売切れ商品数: {yahoo_data['count_sold_out_item']}\n"
                body += f"ステータス変更商品数: {yahoo_data['count_change_status_item']}\n\n"

                if yahoo_data.get('updated_items'):
                    body += "ステータス変更された商品:\n"
                    for item in yahoo_data['updated_items']:
                        body += f"- 商品ID: {item['unique_id']}\n"
                        body += f"  旧ステータス: {item['old_status']} → 新ステータス: {item['new_status']}\n"
                    body += "\n"
            except KeyError as e:
                body += f"データの取得に失敗しました: {str(e)}\n\n"

    body += "=" * 50 + "\n"
    body += "※このメールは自動送信されています。"
    
    return body

def should_run():
    current_hour = datetime.now().hour
    target_hours = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    return current_hour in target_hours

def main():
    if not should_run():
        print("同期実行時間ではありません")
        return

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