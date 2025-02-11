import requests
from django.conf import settings
from api.models import EbayToken, Setting
from datetime import datetime, timedelta
from typing import Optional, Dict
import base64
import logging

logger = logging.getLogger(__name__)

class EbayAuthService:
    """eBayの認証に関するサービスクラス"""
    def __init__(self):
        setting = Setting.get_settings()
        self.client_id = setting.ebay_client_id
        self.client_secret = setting.ebay_client_secret
        self.dev_id = setting.ebay_dev_id
        self.is_sandbox = settings.EBAY_IS_SANDBOX
        self.auth_url = settings.EBAY_SANDBOX_AUTH_URL if self.is_sandbox else settings.EBAY_PRODUCTION_AUTH_URL
        self.api_url = settings.EBAY_SANDBOX_URL if self.is_sandbox else settings.EBAY_PRODUCTION_URL
        self.scopes = settings.EBAY_OAUTH_SCOPES

    def _get_basic_auth(self) -> str:
        """Basic認証用のヘッダー値を生成"""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    def get_auth_url(self) -> str:
        """認証URLを生成"""
        # スコープをスペース区切りの文字列に変換
        scope_string = ' '.join(str(scope).strip() for scope in self.scopes)
        
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': settings.EBAY_REDIRECT_URI,
            'scope': scope_string,
            'prompt': 'login'
        }
        query_string = '&'.join(f'{k}={v}' for k, v in params.items())
        return f"{self.auth_url}?{query_string}"

    def _make_token_request(self, data: Dict) -> Dict:
        """トークンリクエストを実行"""
        token_url = f"{self.api_url}/identity/v1/oauth2/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': self._get_basic_auth()
        }

        try:
            response = requests.post(token_url, headers=headers, data=data)
            response.raise_for_status()  # Raises HTTPError for 4XX/5XX responses
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e.response.text}")
            raise Exception(f"eBay API error: {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error occurred: {str(e)}")
            raise Exception(f"Network error: {str(e)}")

    def get_application_token(self) -> str:
        """アプリケーショントークンを取得"""
        data = {
            'grant_type': 'client_credentials',
            'scope': ' '.join(str(scope).strip() for scope in self.scopes)
        }

        try:
            token_data = self._make_token_request(data)
            return token_data['access_token']
        except Exception as e:
            logger.error(f"Failed to get application token: {str(e)}")
            raise

    def exchange_code_for_token(self, code: str, user_id: int) -> EbayToken:
        """認証コードをユーザートークンと交換"""
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.EBAY_REDIRECT_URI
        }
        try:
            token_data = self._make_token_request(data)
            expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'])
            # 既存のトークンを削除
            EbayToken.objects.filter(user_id=user_id).delete()
            # 新しいトークンを作成
            token = EbayToken.objects.create(
                user_id=user_id,
                access_token=token_data['access_token'],
                refresh_token=token_data['refresh_token'],
                expires_at=expires_at,
                scope=' '.join(str(scope).strip() for scope in self.scopes)
            )
            return token
        except Exception as e:
            logger.error(f"Failed to exchange code for token: {str(e)}")
            raise

    def refresh_token(self, ebay_token: EbayToken) -> Optional[EbayToken]:
        """リフレッシュトークンを使用して新しいアクセストークンを取得"""
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': ebay_token.refresh_token,
            'scope': ebay_token.scope
        }

        try:
            token_data = self._make_token_request(data)
            expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'])

            ebay_token.access_token = token_data['access_token']
            ebay_token.refresh_token = token_data.get('refresh_token', ebay_token.refresh_token)
            ebay_token.expires_at = expires_at
            ebay_token.save()

            return ebay_token
        except Exception as e:
            logger.error(f"Failed to refresh token: {str(e)}")
            return None 