from django.db import models
from django.conf import settings
from api.models.master import YahooAuctionStatus, YahooFreeMarketStatus

class YahooAuction(models.Model):
    """Yahooオークションのモデル"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.ForeignKey(YahooAuctionStatus, on_delete=models.PROTECT)
    unique_id = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True, blank=True)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    end_time = models.DateTimeField()
    update_datetime = models.DateTimeField(auto_now=True)
    insert_datetime = models.DateTimeField(auto_now_add=True)
    insert_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='yahoo_auction_insert_user')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='yahoo_auction_update_user')
    class Meta:
        db_table = 't_yahoo_auction'
        indexes = [
            models.Index(fields=['status']),
        ]

class YahooFreeMarket(models.Model):
    """Yahooフリマのモデル"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.ForeignKey(YahooFreeMarketStatus, on_delete=models.PROTECT)
    unique_id = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True, blank=True)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    update_datetime = models.DateTimeField(auto_now=True)
    insert_datetime = models.DateTimeField(auto_now_add=True)
    insert_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='yahoo_free_market_insert_user')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='yahoo_free_market_update_user')
    class Meta:
        db_table = 't_yahoo_free_market'
        indexes = [
            models.Index(fields=['status']),
        ]
