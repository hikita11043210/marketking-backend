
import requests
import xml.etree.ElementTree as ET
from api.services.ebay.common import Common

class Trading(Common):
    def get_item_specifics(self, ebay_item_id: str, category_tree_id: str):
        """
        Trading APIを使用してItem Specificsを取得
        """
        try:
            endpoint = f"{self.api_url}/ws/api.dll"
            
            headers = self._get_headers()
            headers.update({
                'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
                'X-EBAY-API-CALL-NAME': 'GetItem',
                'X-EBAY-API-SITEID': category_tree_id, 
                'Content-Type': 'text/xml'
            })
            
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
            
            root = ET.fromstring(response.content)
            ns = {'': 'urn:ebay:apis:eBLBaseComponents'}

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
            raise Exception("Item Specificsの取得に失敗しました")

