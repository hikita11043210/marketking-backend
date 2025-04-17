from django.db import models
from django.conf import settings  # settingsをインポート
from .user import User  # Userモデルを直接インポート

class Service(models.Model):
    """サービスマスタ"""
    service_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'm_service'

    def __str__(self):
        return self.service_name

class Countries(models.Model):
    """国マスタ"""
    code = models.CharField(max_length=2, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    zone_fedex = models.IntegerField(null=True, blank=True)
    zone_dhl = models.IntegerField(null=True, blank=True)
    zone_economy = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'm_countries'
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

class ShippingRatesFedex(models.Model):
    """FedEx送料マスタ"""
    zone = models.IntegerField(null=False)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    rate = models.IntegerField(null=False)

    class Meta:
        db_table = 'm_shipping_rates_fedex'
        indexes = [
            models.Index(fields=['zone']),
            models.Index(fields=['weight']),
        ]

    def __str__(self):
        return f"FedEx Zone {self.zone} - {self.weight}kg: {self.rate}円"

class ShippingRatesDhl(models.Model):
    """DHL送料マスタ"""
    zone = models.IntegerField(null=False)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    is_document = models.BooleanField(default=False)
    rate = models.IntegerField(null=False)

    class Meta:
        db_table = 'm_shipping_rates_dhl'
        indexes = [
            models.Index(fields=['zone']),
            models.Index(fields=['weight']),
        ]

    def __str__(self):
        doc_type = "書類" if self.is_document else "物品"
        return f"DHL Zone {self.zone} - {self.weight}kg ({doc_type}): {self.rate}円"

class ShippingRatesEconomy(models.Model):
    """Economy送料マスタ"""
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    rate = models.IntegerField(null=False)

    class Meta:
        db_table = 'm_shipping_rates_economy'
        indexes = [
            models.Index(fields=['weight']),
        ]

    def __str__(self):
        return f"Economy {self.country.name} - {self.weight}kg: {self.rate}円"

class EbayStoreType(models.Model):
    """eBayストアタイプマスタ"""
    store_type = models.CharField(max_length=50, unique=True, null=False)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    monthly_fee_annual = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    free_listings = models.IntegerField(null=False)
    listing_fee_over_limit = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    final_value_fee = models.DecimalField(max_digits=4, decimal_places=1, null=False)
    final_value_fee_category_discount = models.BooleanField(default=False)
    international_fee = models.DecimalField(max_digits=4, decimal_places=2, null=False)

    class Meta:
        db_table = 'm_ebay_store_type'

    def __str__(self):
        return self.store_type

class Tax(models.Model):
    """税率マスタ"""
    rate = models.DecimalField(max_digits=4, decimal_places=2, null=False)

    class Meta:
        db_table = 'm_tax'

    def __str__(self):
        return f"{self.rate}%"

class Setting(models.Model):
    """設定マスタ"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='settings')
    ebay_store_type = models.ForeignKey(EbayStoreType, on_delete=models.PROTECT, related_name='settings')
    yahoo_client_id = models.CharField(max_length=255, null=True, blank=True)
    yahoo_client_secret = models.CharField(max_length=255, null=True, blank=True)
    ebay_client_id = models.CharField(max_length=255, null=True, blank=True)
    ebay_dev_id = models.CharField(max_length=255, null=True, blank=True)
    ebay_client_secret = models.CharField(max_length=255, null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    deepl_api_key = models.CharField(max_length=255, null=True, blank=True)
    description_template_1 = models.TextField(null=True, blank=True)
    description_template_2 = models.TextField(null=True, blank=True)
    description_template_3 = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'm_setting'

    def __str__(self):
        return f"Settings for {self.user.username}"

    @classmethod
    def get_settings(cls, user):
        """ユーザーの設定を取得または作成する"""
        settings, created = cls.objects.get_or_create(user=user)
        return settings

class Status(models.Model):
    """ステータスマスタ"""
    status_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'm_status'

    def __str__(self):
        return self.status_name

class Condition(models.Model):
    """商品状態マスタ"""
    condition_id = models.IntegerField(null=False)
    condition_enum = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'm_condition'

    def __str__(self):
        return f"{self.condition_id} - {self.condition_enum}"

class YahooAuctionStatus(models.Model):
    """Yahooオークションステータスマスタ"""
    status_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'm_yahoo_auction_status'

    def __str__(self):
        return self.status_name

class YahooFreeMarketStatus(models.Model):
    """Yahooフリーマーケットステータスマスタ"""
    status_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'm_yahoo_free_market_status'

    def __str__(self):
        return self.status_name

class TransactionType(models.Model):
    """取引区分マスタ"""
    value = models.CharField(max_length=50, null=False, unique=True)

    class Meta:
        db_table = 'm_transaction_types'

    def __str__(self):
        return self.value