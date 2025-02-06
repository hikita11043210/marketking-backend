from django.core.cache import cache
from django.core.exceptions import ValidationError
import requests
import logging
from typing import Dict, List, Any
from .ebay_auth import EbayAuthService

logger = logging.getLogger(__name__)

class EbayCategoriesService:
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

            url = f"{self.auth_service.base_url}/commerce/taxonomy/v1/{endpoint}"
            
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

    def get_default_category_tree_id(self, marketplace_id: str = 'EBAY_US') -> str:
        """デフォルトのカテゴリーツリーIDを取得"""
        cache_key = f"ebay_category_tree_id_{marketplace_id}"
        cached_id = cache.get(cache_key)
        if cached_id:
            return cached_id

        response = self._make_request(f'get_default_category_tree_id?marketplace_id={marketplace_id}')
        category_tree_id = response.get('categoryTreeId')
        
        if not category_tree_id:
            raise ValidationError("カテゴリーツリーIDの取得に失敗しました")
        
        # 24時間キャッシュ
        cache.set(cache_key, category_tree_id, 86400)
        return category_tree_id

    def get_category_tree(self, category_tree_id: str = None, marketplace_id: str = 'EBAY_US') -> Dict[str, Any]:
        """カテゴリーツリーを取得"""
        if not category_tree_id:
            category_tree_id = self.get_default_category_tree_id(marketplace_id)

        cache_key = f"ebay_category_tree_{category_tree_id}"
        cached_tree = cache.get(cache_key)
        if cached_tree:
            return cached_tree

        response = self._make_request(f'category_tree/{category_tree_id}')
        
        # 24時間キャッシュ
        cache.set(cache_key, response, 86400)
        return response

    def get_category_suggestions(self, query: str, marketplace_id: str = 'EBAY_US') -> List[Dict[str, Any]]:
        """カテゴリーの候補を検索"""
        category_tree_id = self.get_default_category_tree_id(marketplace_id)
        
        response = self._make_request(
            f'category_tree/{category_tree_id}/get_category_suggestions',
            method='POST',
            data={'q': query}
        )
        
        return response.get('categorySuggestions', []) 