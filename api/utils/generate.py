import time
import re

def generate_merchant_location_key(location_name: str = 'default', country_code: str = 'US') -> str:
    """
    インベントリロケーションの一意のキーを生成する
    Args:
        location_name (str): ロケーション名
        country_code (str, optional): 国コード（例：JP, US）
    Returns:
        str: 生成されたマーチャントロケーションキー
    """
    try:
        timestamp = int(time.time() * 1000)
        location_slug = location_name.lower().replace(' ', '_')
        location_slug = re.sub(r'[^a-z0-9_]', '', location_slug)
        country_prefix = f"{country_code.lower()}_" if country_code else ""
        merchant_location_key = f"{country_prefix}{location_slug}_{timestamp}"
        
        if len(merchant_location_key) > 36:
            merchant_location_key = merchant_location_key[:36]
        
        return merchant_location_key
        
    except Exception as e:
        raise Exception("マーチャントロケーションキーの生成に失敗しました")
