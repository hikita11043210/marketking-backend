from api.services.ebay.common import Common
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Category(Common):
    def get_categories(self, category_tree_id: str, query: str):
        """
        カテゴリの検索を行う
        Args:
            query (str): 検索キーワード（カテゴリ名またはID）
        Returns:
            dict: 検索結果
        """
        try:
            endpoint = f"{self.api_url}/commerce/taxonomy/v1/category_tree/{category_tree_id}/get_category_suggestions"
            headers = self._get_headers()
            params = {'q': query}
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            # レスポンスデータを整形
            data = response.json()
            categories = []

            for suggestion in data.get('categorySuggestions', []):
                category = suggestion.get('category', {})
                ancestors = suggestion.get('categoryTreeNodeAncestors', [])
                
                # カテゴリパスを構築
                path = []
                for ancestor in reversed(ancestors):
                    path.append(ancestor.get('categoryName'))
                path.append(category.get('categoryName'))
                
                categories.append({
                    'categoryId': category.get('categoryId'),
                    'categoryName': category.get('categoryName'),
                    'path': ' > '.join(path)
                })
            
            return {
                'success': True,
                'categories': categories
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to search categories: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Error response: {e.response.text}")
            raise Exception("カテゴリの検索に失敗しました")

    def get_all_categories(self):
        """
        全カテゴリを取得する
        Returns:
            dict: カテゴリツリー
        """
        try:
            endpoint = f"{self.api_url}/commerce/taxonomy/v1/category_tree/{settings.EBAY_MARKETPLACE_ID}"
            headers = self._get_headers()
            
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            root_category = data.get('rootCategoryNode', {})
            
            def process_category(category_node):
                """カテゴリノードを再帰的に処理"""
                result = {
                    'categoryId': category_node.get('categoryId'),
                    'categoryName': category_node.get('categoryName'),
                    'leafCategory': category_node.get('leafCategoryNode', False),
                    'level': category_node.get('categoryLevel'),
                    'children': []
                }
                
                # 子カテゴリを処理
                child_nodes = category_node.get('childCategoryTreeNodes', [])
                for child in child_nodes:
                    result['children'].append(process_category(child))
                
                return result
            
            return {
                'success': True,
                'categoryTree': process_category(root_category)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get category tree: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Error response: {e.response.text}")
            raise Exception("カテゴリツリーの取得に失敗しました")

    def get_categories_tree_id(self):
        """
        カテゴリツリーIDを取得する
        Returns:
            str: カテゴリツリーID
        """
        try:
            endpoint = f"{self.api_url}/commerce/taxonomy/v1/get_default_category_tree_id?marketplace_id={settings.EBAY_MARKETPLACE_ID}"
            headers = self._get_headers()
            
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            
            # レスポンスデータを整形
            data = response.json()
            return data.get('categoryTreeId')
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get category tree id: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Error response: {e.response.text}")
            raise Exception("カテゴリツリーIDの取得に失敗しました")


    def get_category_aspects(self, category_id: str):
        """
        カテゴリIDからアスペクト情報（商品の属性情報）を取得する
        Args:
            category_id (str): カテゴリID
        Returns:
            dict: アスペクト情報
        """
        try:
            endpoint = f"{self.api_url}/commerce/taxonomy/v1/category_tree/{settings.EBAY_API_SITE_ID}/get_item_aspects_for_category"
            headers = self._get_headers()
            params = {'category_id': category_id}
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                raise Exception(f"カテゴリのアスペクト情報の取得に失敗しました: {e.response.text}")
            raise Exception("カテゴリのアスペクト情報の取得に失敗しました")
