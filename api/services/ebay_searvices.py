from api.services.ebay_auth import EbayAuthService
import requests
from django.conf import settings
import logging
import xml.etree.ElementTree as ET

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

    def search_categories(self, query: str):
        """
        カテゴリの検索を行う
        Args:
            query (str): 検索キーワード（カテゴリ名またはID）
        Returns:
            dict: 検索結果
        """
        try:
            endpoint = f"{self.api_url}/commerce/taxonomy/v1/category_tree/{settings.EBAY_API_SITE_ID}/get_category_suggestions"
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
            endpoint = f"{self.api_url}/commerce/taxonomy/v1/category_tree/{settings.EBAY_API_SITE_ID}"
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

    def get_item_specifics(self, ebay_item_id: str):
        """
        Trading APIを使用してItem Specificsを取得
        """
        try:
            # 正しいエンドポイントURLに修正
            endpoint = f"{self.api_url}/ws/api.dll"
            
            headers = self._get_headers()
            headers.update({
                'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
                'X-EBAY-API-CALL-NAME': 'GetItem',
                'X-EBAY-API-SITEID': str(settings.EBAY_API_SITE_ID), 
                'Content-Type': 'text/xml'
            })
            
            # XMLリクエストの修正
            request_xml = f"""<?xml version="1.0" encoding="utf-8"?>
                <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
                    <RequesterCredentials>
                        <eBayAuthToken>{self.auth_service.get_user_token().access_token}</eBayAuthToken>
                    </RequesterCredentials>
                    <ItemID>{ebay_item_id}</ItemID>
                    <DetailLevel>ReturnAll</DetailLevel>
                    <IncludeItemSpecifics>true</IncludeItemSpecifics>
                </GetItemRequest>"""
            
            response = requests.post(endpoint, headers=headers, data=request_xml)
            response.raise_for_status()
            # XMLレスポンスの解析
            root = ET.fromstring(response.content)
            ns = {'': 'urn:ebay:apis:eBLBaseComponents'}  # デフォルト名前空間を定義

            item_specifics = []
            for specifics in root.findall('.//ItemSpecifics', ns):
                for name_value in specifics.findall('NameValueList', ns):
                    name = name_value.find('Name', ns).text
                    values = [v.text for v in name_value.findall('Value', ns)]
                    item_specifics.append({'name': name, 'values': values})

            category_id = root.findtext('.//PrimaryCategoryID', ns)
            return {
                'success': True,
                'message': 'Item Specificsの取得に成功しました',
                'data': {
                    'item_specifics': item_specifics,
                    'category_id': category_id
                }
            }

        except Exception as e:
            logger.error(f"Trading API Error: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }

