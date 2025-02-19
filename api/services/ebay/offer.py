from api.services.ebay.common import Common
import requests

class Offer(Common):
    def create_offer(self, offer_data: dict):
        """
        商品の出品情報を作成する
        Args:
            offer_data (dict): 出品情報
        Returns:
            dict: レスポンス（offerId含む）
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/offer"
            headers = self._get_headers()
            response = requests.post(endpoint, headers=headers, json=offer_data)
            response.raise_for_status()
            
            return {
                'success': True,
                'message': '出品情報の作成に成功しました',
                'data': response.json()
            }
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                raise Exception(f"出品情報の作成に失敗しました: {e.response.text}")
            raise Exception("出品情報の作成に失敗しました")


    def delete_offer(self, offer_id: str):
        """
        オファーを削除する
        Args:
            offer_id (str): 削除するオファーのID
        Returns:
            dict: レスポンス
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/offer/{offer_id}"
            headers = self._get_headers()
            response = requests.delete(endpoint, headers=headers)
            response.raise_for_status()
            
            return {
                'success': True,
                'message': 'オファーの削除に成功しました'
            }
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                raise Exception(f"オファーの削除に失敗しました: {e.response.text}")
            raise Exception("オファーの削除に失敗しました")


    def publish_offer(self, offer_id: str):
        """
        出品をアクティブ化する
        Args:
            offer_id (str): オファーID
        Returns:
            dict: レスポンス（listingId含む）
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/offer/{offer_id}/publish"
            headers = self._get_headers()
            requests.post(endpoint, headers=headers)
            
        except requests.exceptions.RequestException as e:
            self.delete_offer(offer_id)
            if hasattr(e.response, 'text'):
                raise Exception(f"商品の出品に失敗しました: {e.response.text}")
            raise Exception("商品の出品に失敗しました")
