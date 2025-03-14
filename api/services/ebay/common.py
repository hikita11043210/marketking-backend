from api.services.ebay.auth import EbayAuthService
from django.conf import settings

class Common:
    def __init__(self, user):
        self.auth_service = EbayAuthService(user)
        self.user = user
        self.api_url = settings.EBAY_SANDBOX_URL if settings.EBAY_IS_SANDBOX else settings.EBAY_PRODUCTION_URL
        self.marketplace_id = settings.EBAY_MARKETPLACE_ID

    def _get_headers(self):
        """APIリクエスト用のヘッダーを取得"""
        # ユーザーのeBayトークンを取得
        ebay_token = self.auth_service.get_user_token()
        if not ebay_token:
            raise Exception("eBayとの連携が必要です")
            
        return {
            'Authorization': f'Bearer {ebay_token.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "Content-Language": "en-US",
            "Accept-Language": "en-US"
        }
