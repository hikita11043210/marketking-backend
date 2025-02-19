from api.services.ebay.common import Common
import requests
from django.conf import settings

class Marketplace(Common):
    def get_category_conditions(self, category_id: str):
        """
        カテゴリIDから利用可能なコンディション情報を取得する
        Args:
            category_id (str): カテゴリID
        Returns:
            dict: コンディション情報のリスト
        """
        try:
            endpoint = f"{self.api_url}/sell/metadata/v1/marketplace/{settings.EBAY_MARKETPLACE_ID}/get_item_condition_policies"
            headers = self._get_headers()
                        
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()
            print(data)
            conditions = [
                policy["itemConditions"]
                for policy in data["itemConditionPolicies"]
                if category_id in policy["categoryId"]
            ]
            return conditions

        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                raise Exception(f"カテゴリのコンディション情報の取得に失敗しました: {e.response.text}")
            raise Exception("カテゴリのコンディション情報の取得に失敗しました")
