from django.db import models
from django.conf import settings
from api.utils.encryption import encrypt_value, decrypt_value

class EbayToken(models.Model):
    """eBayのアクセストークンを管理するモデル"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    _access_token = models.TextField(db_column='access_token')
    _refresh_token = models.TextField(db_column='refresh_token')
    expires_at = models.DateTimeField()
    scope = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def access_token(self):
        return decrypt_value(self._access_token)

    @access_token.setter
    def access_token(self, value):
        self._access_token = encrypt_value(value)

    @property
    def refresh_token(self):
        return decrypt_value(self._refresh_token)

    @refresh_token.setter
    def refresh_token(self, value):
        self._refresh_token = encrypt_value(value)

    class Meta:
        db_table = 'ebay_tokens' 