from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
import requests
import logging

logger = logging.getLogger(__name__)

class CurrencyService:
    CACHE_KEY_PREFIX = 'exchange_rate'
    CACHE_TIMEOUT = 3600  # 1時間

    @classmethod
    def get_exchange_rate(cls, from_currency: str, to_currency: str) -> float:
        """
        指定された通貨ペアの為替レートを取得
        
        Args:
            from_currency: 変換元通貨コード（例：'JPY'）
            to_currency: 変換先通貨コード（例：'USD'）
            
        Returns:
            float: 為替レート
        """
        cache_key = f"{cls.CACHE_KEY_PREFIX}:{from_currency}:{to_currency}"
        rate = cache.get(cache_key)
        
        if rate is not None:
            return rate

        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url, params={'key': settings.EXCHANGE_RATE_API_KEY})
            response.raise_for_status()
            
            data = response.json()
            rate = data['rates'].get(to_currency)
            
            if rate is None:
                raise ValidationError(f"為替レートが見つかりません: {from_currency}/{to_currency}")
            
            # レートをキャッシュに保存
            cache.set(cache_key, rate, cls.CACHE_TIMEOUT)
            
            return rate
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get exchange rate: {str(e)}")
            return 0

    @staticmethod
    def get_default_rate(from_currency: str, to_currency: str) -> float:
        """デフォルトの為替レートを取得"""
        default_rates = {
            'JPY': {
                'USD': 0.0067,  # 1 JPY = 0.0067 USD
            },
            'USD': {
                'JPY': 150,  # 1 USD = 150 JPY
            }
        }
        
        try:
            return default_rates[from_currency][to_currency]
        except KeyError:
            raise ValidationError(f"サポートされていない通貨ペアです: {from_currency}/{to_currency}")