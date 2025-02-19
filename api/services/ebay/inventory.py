from api.services.ebay.common import Common
import requests

class Inventory(Common):
    def create_inventory_item(self, sku: str, product_data: dict):
        """
        商品情報を登録する
        Args:
            sku (str): 商品のSKU
            product_data (dict): 商品情報
        Returns:
            dict: レスポンス
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/inventory_item/{sku}"
            params = {'marketplace_id': self.marketplace_id}
            headers = self._get_headers()
            
            response = requests.put(endpoint, headers=headers, json=product_data, params=params)
            response.raise_for_status()

            return {
                'success': True,
                'message': '商品情報の登録に成功しました',
                'data': response.json() if response.text else None
            }
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                raise Exception(f"商品情報の登録に失敗しました: {e.response.text}")
            raise Exception("商品情報の登録に失敗しました")


    def get_inventory_locations(self, limit: int = None, offset: int = None):
        """
        すべてのインベントリロケーション情報を取得する
        Args:
            limit (int, optional): 1ページあたりの最大取得件数
            offset (int, optional): 取得開始位置
        Returns:
            dict: レスポンス
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/location"
            headers = self._get_headers()
            
            params = {}
            if limit is not None:
                params['limit'] = limit
            if offset is not None:
                params['offset'] = offset
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                raise Exception(f"インベントリロケーション情報の取得に失敗しました: {e.response.text}")
            raise Exception("インベントリロケーション情報の取得に失敗しました")


    def create_inventory_location(self, merchant_location_key: str, location_data: dict):
        """
        インベントリロケーションを作成する
        Args:
            merchant_location_key (str): ロケーションの一意のキー
            location_data (dict): ロケーション情報
            {
                "location": {
                    "address": {
                        "addressLine1": "住所1",
                        "addressLine2": "住所2",
                        "city": "市区町村",
                        "stateOrProvince": "都道府県",
                        "postalCode": "郵便番号",
                        "country": "国コード"
                    }
                },
                "locationTypes": ["WAREHOUSE"],  # STORE, WAREHOUSE, FULFILLMENT_CENTER
                "name": "ロケーション名",
                "merchantLocationStatus": "ENABLED",  # ENABLED, DISABLED
                "locationInstructions": "ロケーションの説明",
                "phone": "電話番号"
            }

            とりあえず登録したデータ
            location_data = {
                "location": {
                    "address": {
                        "addressLine1": "Higashiakuragawa",
                        "addressLine2": "62-29",
                        "city": "Yokkaichishi",
                        "stateOrProvince": "Mie",
                        "postalCode": "5100805",
                        "country": "JP"
                    }
                },
                "locationTypes": ["WAREHOUSE"],  # STORE, WAREHOUSE, FULFILLMENT_CENTER
                "name": "house",
                "merchantLocationStatus": "ENABLED",  # ENABLED, DISABLED
                "locationInstructions": "my house",
                "phone": "09098934062"
            }

        Returns:
            dict: レスポンス
        """
        try:
            merchant_location_key = self.generate_merchant_location_key()
            endpoint = f"{self.api_url}/sell/inventory/v1/location/{merchant_location_key}"
            headers = self._get_headers()
            
            response = requests.post(endpoint, headers=headers, json=location_data)
            response.raise_for_status()
            
            return {
                'success': True,
                'message': 'インベントリロケーションの作成に成功しました',
                'data': response.json() if response.text else None
            }
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                raise Exception(f"インベントリロケーションの作成に失敗しました: {e.response.text}")
            raise Exception("インベントリロケーションの作成に失敗しました")