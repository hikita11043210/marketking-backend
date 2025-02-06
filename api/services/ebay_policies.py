from django.core.cache import cache
from django.core.exceptions import ValidationError
import requests
import logging
from typing import Dict, List, Any
from .ebay_auth import EbayAuthService

logger = logging.getLogger(__name__)

class EbayPoliciesService:
    def __init__(self, user_id: int):
        self.auth_service = EbayAuthService(user_id)
        self.user_id = user_id

    def _make_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict:
        """APIリクエストを実行"""
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_service.get_access_token()}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            url = f"{self.auth_service.base_url}/sell/account/v1/{endpoint}"
            
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            if not response.ok:
                logger.error(f"API request failed: {response.status_code}")
                logger.error(f"Response: {response.content.decode('utf-8')}")
                raise ValidationError("APIリクエストに失敗しました")

            return response.json()

        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise ValidationError("APIリクエストに失敗しました")

    def get_fulfillment_policies(self, marketplace_id: str = 'EBAY_US') -> List[Dict[str, Any]]:
        """出荷ポリシーの一覧を取得"""
        cache_key = f"ebay_fulfillment_policies_{self.user_id}_{marketplace_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        response = self._make_request(f'fulfillment_policy?marketplace_id={marketplace_id}')
        policies = response.get('fulfillmentPolicies', [])
        
        # 1時間キャッシュ
        cache.set(cache_key, policies, 3600)
        return policies

    def get_payment_policies(self, marketplace_id: str = 'EBAY_US') -> List[Dict[str, Any]]:
        """支払いポリシーの一覧を取得"""
        cache_key = f"ebay_payment_policies_{self.user_id}_{marketplace_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        response = self._make_request(f'payment_policy?marketplace_id={marketplace_id}')
        policies = response.get('paymentPolicies', [])
        
        # 1時間キャッシュ
        cache.set(cache_key, policies, 3600)
        return policies

    def get_return_policies(self, marketplace_id: str = 'EBAY_US') -> List[Dict[str, Any]]:
        """返品ポリシーの一覧を取得"""
        cache_key = f"ebay_return_policies_{self.user_id}_{marketplace_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        response = self._make_request(f'return_policy?marketplace_id={marketplace_id}')
        policies = response.get('returnPolicies', [])
        
        # 1時間キャッシュ
        cache.set(cache_key, policies, 3600)
        return policies

    def get_all_policies(self, marketplace_id: str = 'EBAY_US') -> Dict[str, List[Dict[str, Any]]]:
        """全てのポリシーを一括取得"""
        return {
            'fulfillment_policies': self.get_fulfillment_policies(marketplace_id),
            'payment_policies': self.get_payment_policies(marketplace_id),
            'return_policies': self.get_return_policies(marketplace_id)
        } 