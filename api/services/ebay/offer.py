from api.services.ebay.common import Common
import requests
import json
from django.http import JsonResponse
import logging

class Offer(Common):
    def get_offer_status(self, sku: str):
        """
        商品の出品状態を取得する
        Returns:
            - PUBLISHED: 出品中
            - UNPUBLISHED: 取り下げ
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/offer"
            params = {
                'sku': sku,
                'marketplace_id': self.marketplace_id
            }
            headers = self._get_headers()
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            offers = response.json().get('offers', [])

            if not offers:
                return None

            return offers[0].get('status')
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"オファー情報の取得に失敗しました: {str(e)}")


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
            
            return response.json()
            
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
        注意：
            - オファーデータが削除されてしまうため、利用すると"publish_offer"による再登録は不可能なので基本的に利用しない
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
        注意：
            - 再出品時もこの関数を使用する
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/offer/{offer_id}/publish"
            headers = self._get_headers()
            response = requests.post(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            error_detail = f"Status code: {e.response.status_code} - {e.response.text}"
            if e.response.status_code == 400:
                error_detail += "\nよくある原因:\n1. オファーが既にPUBLISHED状態\n2. 必須フィールド不足\n3. 価格/在庫数が不正"
            raise Exception(f"商品の出品に失敗しました: {error_detail}")
        except Exception as e:
            raise Exception(f"予期せぬエラーが発生しました: {str(e)}")


    def withdraw_offer(self, offer_id: str):
        """
        出品を取り下げる（アンパブリッシュする）
        Args:
            offer_id (str): 取り下げる出品のオファーID
        Returns:
            dict: レスポンス
        注意：
            - 画面での取下げ操作と同じ。商品が削除されることはない。（出品状態を解除するときは基本的にはこの操作でOK）
        """
        try:
            endpoint = f"{self.api_url}/sell/inventory/v1/offer/{offer_id}/withdraw"
            headers = self._get_headers()
            
            response = requests.post(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                raise Exception(f"出品の取り下げに失敗しました: {e.response.text}")
            raise Exception("出品の取り下げに失敗しました")

    def end_fixed_price_item(self, item_id):
        """
        Trading APIを使用して商品を「終了済み」にする
        Args:
            item_id (str): 終了する商品のeBay商品ID
        Returns:
            dict: 処理結果
        """
        try:
            endpoint = f"{self.api_url}/ws/api.dll"
            
            headers = self._get_headers()
            headers.update({
                'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
                'X-EBAY-API-CALL-NAME': 'EndFixedPriceItem',
                'X-EBAY-API-SITEID': '0',  # US
                'Content-Type': 'text/xml'
            })
            
            request_xml = f"""<?xml version="1.0" encoding="utf-8"?>
                <EndFixedPriceItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
                    <RequesterCredentials>
                        <eBayAuthToken>{self.auth_service.get_user_token().access_token}</eBayAuthToken>
                    </RequesterCredentials>
                    <ItemID>{item_id}</ItemID>
                    <EndingReason>NotAvailable</EndingReason>
                </EndFixedPriceItemRequest>"""
            
            response = requests.post(endpoint, headers=headers, data=request_xml)
            response.raise_for_status()
            
            return {
                'success': True,
                'message': '商品を終了済みにしました'
            }
            
        except Exception as e:
            raise Exception(f"商品の終了処理に失敗しました: {str(e)}")

    def delete_ended_item(self, item_id):
        """
        Trading APIを使用して終了済み商品をユーザーインターフェースから削除する
        現在のeBay APIではDeleteFixedPriceItemがサポートされていないため、
        終了済みにすることで対応します。
        
        Args:
            item_id (str): 削除する商品のeBay商品ID
        Returns:
            dict: 処理結果
        """
        logger = logging.getLogger(__name__)
        logger.info(f"終了済み商品の削除を試みます: item_id={item_id}")
        
        try:
            # DeleteFixedPriceItemがサポートされていないため、
            # 代わりにEndFixedPriceItemを使用して終了済みにする
            result = self.end_fixed_price_item(item_id)
            
            logger.info(f"終了済み商品をend_fixed_price_itemで処理しました: item_id={item_id}")
            return {
                'success': True,
                'message': '終了済み商品を削除しました（終了済み状態に変更）'
            }
        except Exception as e:
            logger.error(f"終了済み商品の削除に失敗しました: {str(e)}")
            raise Exception(f"終了済み商品の削除に失敗しました: {str(e)}")