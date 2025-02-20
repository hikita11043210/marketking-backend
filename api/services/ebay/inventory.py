from api.services.ebay.common import Common
import requests
from api.utils.generate import generate_merchant_location_key

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

            return response.json() if response.text else None
            
        except requests.exceptions.RequestException as e:
            return Exception(f"商品情報の登録に失敗しました: {e.response.text}")


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
            raise Exception(f"インベントリロケーション情報の取得に失敗しました: {str(e)}")


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
            merchant_location_key = generate_merchant_location_key()
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
        

    def get_inventory_items(self, status_filter: str = None):
        """
        ステータス別にインベントリアイテムを取得
        Args:
            status_filter (str, optional): フィルタ条件（ACTIVE/INACTIVEなど）
        Returns:
            list: 商品リスト
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/inventory_item"
            headers = self._get_headers()
            params = {'marketplace_id': self.marketplace_id}
            
            if status_filter:
                params['status'] = status_filter
            
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            return response.json().get('inventoryItems', [])
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"get_inventory_items:商品情報の取得に失敗しました: {str(e)}")


    def get_inventory_item_for_sku(self, sku: str):
        """
        ステータス別にインベントリアイテムを取得
        Args:
            sku (str): 商品のSKU
        Returns:
            list: 商品
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/inventory_item/{sku}"
            headers = self._get_headers()
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            # 商品が見つからない場合はNoneを返す
            return None

    def delete_inventory_item(self, sku: str):
        """
        SKUを指定して商品情報を削除する
        Args:
            sku (str): 削除する商品のSKU
        Returns:
            dict: 処理結果
        注意：
            - 関連する未公開のオファーも削除される
            - 関連するeBayの出品も削除される
            - バリエーション商品の場合、そのSKUのみ削除される
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/inventory_item/{sku}"
            headers = self._get_headers()
            
            response = requests.delete(endpoint, headers=headers)
            response.raise_for_status()
            
            return {
                'success': True,
                'message': f'SKU: {sku} の商品情報を削除しました'
            }
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                return f"商品情報の削除に失敗しました: {e.response.text}"
            return f"商品情報の削除に失敗しました: {str(e)}"