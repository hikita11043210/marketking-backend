from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
import requests
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta
from django.utils import timezone
from ..models import Setting

logger = logging.getLogger(__name__)

class EbayAuthService:
    def __init__(self):
        try:
            setting = Setting.objects.get()
            if not all([
                setting.ebay_client_id,
                setting.ebay_client_secret,
                setting.ebay_dev_id
            ]):
                missing_fields = []
                if not setting.ebay_client_id:
                    missing_fields.append("Client ID")
                if not setting.ebay_client_secret:
                    missing_fields.append("Client Secret")
                if not setting.ebay_dev_id:
                    missing_fields.append("Dev ID")
                raise ValidationError(f"以下のeBay認証情報が設定されていません: {', '.join(missing_fields)}")
            
            self.client_id = setting.ebay_client_id
            self.client_secret = setting.ebay_client_secret
            self.dev_id = setting.ebay_dev_id
            self.is_sandbox = getattr(settings, 'EBAY_IS_SANDBOX', True)
            self.base_url = getattr(settings, 'EBAY_SANDBOX_URL') if self.is_sandbox else getattr(settings, 'EBAY_PRODUCTION_URL')
            
        except Setting.DoesNotExist:
            raise ValidationError("eBayの認証情報が設定されていません。各種設定画面で設定してください。")
        except Exception as e:
            logger.error(f"Failed to initialize EbayAuthService: {str(e)}")
            raise

    def get_authorization_url(self, state: str = '') -> str:
        """認可URLを生成"""
        try:
            # redirect_uriが設定されているか確認
            if not settings.EBAY_REDIRECT_URI:
                logger.error("EBAY_REDIRECT_URI is not set")
                raise ValidationError("リダイレクトURLが設定されていません")

            # scopeが設定されているか確認
            if not settings.EBAY_OAUTH_SCOPES:
                logger.error("EBAY_OAUTH_SCOPES is not set")
                raise ValidationError("OAuth scopeが設定されていません")

            params = {
                'client_id': self.client_id,
                'response_type': 'code',
                'redirect_uri': settings.EBAY_REDIRECT_URI,
                'scope': ' '.join(settings.EBAY_OAUTH_SCOPES),
                'prompt': 'login',
                'state': state
            }
            
            # URLエンコード（スコープは特別な処理が必要）
            encoded_params = []
            for k, v in params.items():
                if k == 'scope':
                    # スコープは空白文字をそのまま保持
                    encoded_value = requests.utils.quote(str(v), safe=' ')
                else:
                    encoded_value = requests.utils.quote(str(v))
                encoded_params.append(f'{k}={encoded_value}')
            
            # Sandboxの場合はURLを変更
            auth_url = 'https://auth.sandbox.ebay.com/oauth2/authorize' if self.is_sandbox else 'https://auth.ebay.com/oauth2/authorize'
            final_url = f"{auth_url}?{'&'.join(encoded_params)}"
            
            logger.info(f"Generated OAuth URL: {final_url}")  # URLをログに出力
            return final_url
            
        except Exception as e:
            logger.error(f"Failed to generate authorization URL: {str(e)}")
            raise ValidationError("認可URLの生成に失敗しました")

    def exchange_code_for_tokens(self, code: str) -> Dict[str, str]:
        """認可コードをトークンと交換"""
        try:
            # redirect_uriが設定されているか確認
            if not settings.EBAY_REDIRECT_URI:
                raise ValidationError("リダイレクトURLが設定されていません")


            token_url = f"{self.base_url}/identity/v1/oauth2/token"
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': settings.EBAY_REDIRECT_URI
            }
            
            response = requests.post(
                token_url,
                data=data,
                auth=(self.client_id, self.client_secret),
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if not response.ok:
                logger.error(f"Token exchange failed: {response.status_code}")
                logger.error(f"Response: {response.content.decode('utf-8')}")
                raise ValidationError("トークンの取得に失敗しました1")

            token_data = response.json()
            
            # トークンを保存
            setting = Setting.objects.get()
            setting.ebay_access_token = token_data.get('access_token')
            setting.ebay_refresh_token = token_data.get('refresh_token')
            setting.ebay_token_expires_at = timezone.now() + timedelta(seconds=token_data.get('expires_in', 7200))
            setting.save()
            
            return {
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token'),
                'expires_in': token_data.get('expires_in')
            }
            
        except Exception as e:
            logger.error(f"Failed to exchange code for tokens: {str(e)}")
            raise ValidationError("トークンの取得に失敗しました2")


    def get_access_token(self) -> str:
        """アクセストークンを取得（必要に応じてリフレッシュ）"""
        try:
            setting = Setting.objects.get()
            
            # アクセストークンが存在しない場合はエラー
            if not setting.ebay_access_token:
                raise ValidationError("eBayとの連携が必要です")

            # トークンの有効期限をチェック
            if setting.ebay_token_expires_at and setting.ebay_token_expires_at > timezone.now():
                return setting.ebay_access_token

            # リフレッシュトークンが存在しない場合はエラー
            if not setting.ebay_refresh_token:
                raise ValidationError("eBayとの再連携が必要です")

            # トークンをリフレッシュ
            token_url = f"{self.base_url}/identity/v1/oauth2/token"
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': setting.ebay_refresh_token,
            }
            
            response = requests.post(
                token_url,
                data=data,
                auth=(self.client_id, self.client_secret),
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if not response.ok:
                logger.error(f"Token refresh failed: {response.status_code}")
                logger.error(f"Response: {response.content.decode('utf-8')}")
                raise ValidationError("トークンの更新に失敗しました")

            token_data = response.json()
            
            # 新しいトークンを保存
            setting.ebay_access_token = token_data.get('access_token')
            if token_data.get('refresh_token'):  # リフレッシュトークンも更新される場合
                setting.ebay_refresh_token = token_data.get('refresh_token')
            setting.ebay_token_expires_at = timezone.now() + timedelta(seconds=token_data.get('expires_in', 7200))
            setting.save()

            return setting.ebay_access_token
            
        except Setting.DoesNotExist:
            raise ValidationError("eBayの認証情報が設定されていません")
        except Exception as e:
            logger.error(f"Failed to get access token: {str(e)}")
            raise ValidationError("アクセストークンの取得に失敗しました") 