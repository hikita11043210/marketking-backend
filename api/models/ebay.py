from django.db import models
from django.conf import settings
from api.utils.encryption import encrypt_value, decrypt_value
from api.models.master import Status
from api.models.yahoo import YahooAuction, YahooFreeMarket

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

class Ebay(models.Model):
    """eBayのモデル"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255, unique=True)
    item_id = models.CharField(max_length=255, null=True, blank=True)
    offer_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2)
    final_profit = models.DecimalField(max_digits=10, decimal_places=2)
    view_count = models.IntegerField(default=0)
    watch_count = models.IntegerField(default=0)
    yahoo_auction_id = models.ForeignKey(YahooAuction, on_delete=models.PROTECT, null=True, blank=True)
    yahoo_free_market_id = models.ForeignKey(YahooFreeMarket, on_delete=models.PROTECT, null=True, blank=True)
    update_datetime = models.DateTimeField(auto_now=True)
    insert_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_ebay'
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['status']),
        ]
