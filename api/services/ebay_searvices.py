from api.services.ebay_auth import EbayAuthService
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EbayService:
    def __init__(self, user):
        self.auth_service = EbayAuthService(user)
        self.user = user
        self.api_url = settings.EBAY_SANDBOX_URL if settings.EBAY_IS_SANDBOX else settings.EBAY_PRODUCTION_URL
        self.marketplace_id = settings.EBAY_MARKETPLACE_ID

    def _get_headers(self):
        """APIリクエスト用のヘッダーを取得"""
        # ユーザーのeBayトークンを取得
        ebay_token = self.auth_service.get_user_token()
        if not ebay_token:
            raise Exception("eBayとの連携が必要です")
            
        return {
            'Authorization': f'Bearer {ebay_token.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get_payment_policies(self):
        """支払いポリシーを取得"""
        try:
            endpoint = f"{self.api_url}/sell/account/v1/payment_policy"
            params = {'marketplace_id': self.marketplace_id}
            headers = self._get_headers()
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get payment policies: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Error response: {e.response.text}")
            raise Exception("支払いポリシーの取得に失敗しました")

    def get_return_policies(self):
        """返品ポリシーを取得"""
        try:
            endpoint = f"{self.api_url}/sell/account/v1/return_policy"
            params = {'marketplace_id': self.marketplace_id}
            headers = self._get_headers()
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get return policies: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Error response: {e.response.text}")
            raise Exception("返品ポリシーの取得に失敗しました")

    def get_fulfillment_policies(self):
        """配送ポリシーを取得"""
        try:
            endpoint = f"{self.api_url}/sell/account/v1/fulfillment_policy"
            params = {'marketplace_id': self.marketplace_id}
            headers = self._get_headers()
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get fulfillment policies: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Error response: {e.response.text}")
            raise Exception("配送ポリシーの取得に失敗しました")

