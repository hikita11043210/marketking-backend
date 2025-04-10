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

    def get_category_aspects(self, category_id: str, category_tree_id: str):
        """
        Taxonomy APIを使用してカテゴリーのアスペクト情報を取得
        
        Args:
            category_id (str): カテゴリーID
            category_tree_id (str): カテゴリーツリーID
            
        Returns:
            dict: 必須アスペクト名のリストを含む辞書
        """
        try:
            endpoint = f"{self.api_url}/commerce/taxonomy/v1/category_tree/{category_tree_id}/get_item_aspects_for_category"
            headers = self._get_headers()
            headers.update({
                'Accept': 'application/json',
                'Accept-Encoding': 'application/gzip'
            })
            
            # クエリパラメータをURLに直接追加
            endpoint = f"{endpoint}?category_id={category_id}"
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            
            # 必須項目（aspectRequired: true）のlocalizedAspectNameのみを抽出
            required_aspects = [
                aspect['localizedAspectName']
                for aspect in response_data.get('aspects', [])
                if aspect.get('aspectConstraint', {}).get('aspectRequired', False)
            ]
            
            return required_aspects
            
        except Exception as e:
            raise Exception(f"カテゴリーアスペクトの取得に失敗しました: {str(e)}")


    def get_item_watch_count(self, ebay_item_id: str):
        """
        Trading APIを使用してアイテムのウォッチ数を取得
        """
        try:
            endpoint = f"{self.api_url}/ws/api.dll"
            
            headers = self._get_headers()
            headers.update({
                'X-EBAY-API-COMPATIBILITY-LEVEL': '967',
                'X-EBAY-API-CALL-NAME': 'GetItem',
                'X-EBAY-API-SITEID': '0', # US
                'Content-Type': 'text/xml'
            })
            
            request_xml = f"""<?xml version="1.0" encoding="utf-8"?>
                <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
                    <RequesterCredentials>
                        <eBayAuthToken>{self.auth_service.get_user_token().access_token}</eBayAuthToken>
                    </RequesterCredentials>
                    <ItemID>{ebay_item_id}</ItemID>
                    <DetailLevel>ReturnAll</DetailLevel>
                    <IncludeWatchCount>true</IncludeWatchCount>
                </GetItemRequest>"""
            
            response = requests.post(endpoint, headers=headers, data=request_xml)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            ns = {'': 'urn:ebay:apis:eBLBaseComponents'}

            # ウォッチ数を取得
            watch_count_elem = root.find('.//WatchCount', ns)
            if watch_count_elem is not None:
                return int(watch_count_elem.text)
            return 0

        except Exception as e:
            raise Exception(f"ウォッチ数の取得に失敗しました: {str(e)}")