from django.core.exceptions import ValidationError
import requests
import logging
from typing import Dict, Any
from .ebay_auth import EbayAuthService

logger = logging.getLogger(__name__)

class EbayInventoryService:
    def __init__(self):
        self.auth_service = EbayAuthService()

    def _make_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict:
        """APIリクエストを実行"""
        try:
            headers = {
                'Authorization': f'Bearer {self.auth_service.get_access_token()}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            url = f"{self.auth_service.base_url}/sell/inventory/v1/{endpoint}"
            
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            if not response.ok:
                logger.error(f"API request failed: {response.status_code}")
                logger.error(f"Response: {response.content.decode('utf-8')}")
                raise ValidationError("APIリクエストに失敗しました")

            return response.json() if response.content else {}

        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise ValidationError("APIリクエストに失敗しました")

    def create_inventory_item(self, product_data: Dict[str, Any]) -> str:
        """在庫アイテムを作成"""
        try:
            # SKUを生成（ここでは簡単な例として現在時刻を使用）
            from datetime import datetime
            sku = f"SKU_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # 在庫アイテムデータを作成
            inventory_item = {
                'product': {
                    'title': product_data['title'],
                    'description': product_data['description'],
                    'aspects': product_data.get('aspects', {}),
                    'brand': product_data.get('brand', ''),
                    'mpn': product_data.get('mpn', '')
                },
                'condition': product_data['condition'],
                'availability': {
                    'shipToLocationAvailability': {
                        'quantity': int(product_data['quantity'])
                    }
                }
            }
            
            # 在庫アイテムを作成
            self._make_request(f'inventory_item/{sku}', method='PUT', data=inventory_item)
            
            # オファーを作成
            offer_data = {
                'sku': sku,
                'marketplaceId': 'EBAY_US',
                'format': 'FIXED_PRICE',
                'availableQuantity': int(product_data['quantity']),
                'categoryId': product_data['categoryId'],
                'listingDescription': product_data['description'],
                'listingPolicies': {
                    'fulfillmentPolicyId': product_data['fulfillmentPolicyId'],
                    'paymentPolicyId': product_data['paymentPolicyId'],
                    'returnPolicyId': product_data['returnPolicyId']
                },
                'pricingSummary': {
                    'price': {
                        'currency': product_data['currency'],
                        'value': str(product_data['price'])
                    }
                },
                'quantityLimitPerBuyer': 1
            }
            
            # オファーを作成
            offer_response = self._make_request('offer', method='POST', data=offer_data)
            
            # オファーを公開
            if 'offerId' in offer_response:
                publish_data = {
                    'offerIds': [offer_response['offerId']]
                }
                self._make_request('offer/publish', method='POST', data=publish_data)
                
                return offer_response['offerId']
            else:
                raise ValidationError("オファーの作成に失敗しました")
            
        except Exception as e:
            logger.error(f"Failed to create inventory item: {str(e)}")
            raise ValidationError("商品の登録に失敗しました") 