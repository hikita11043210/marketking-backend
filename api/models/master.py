from django.db import models
from django.conf import settings  # settingsをインポート
from .user import User  # Userモデルを直接インポート

class Service(models.Model):
    service_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'm_service'

    def __str__(self):
        return self.service_name

class Countries(models.Model):
    country_code = models.CharField(max_length=2, unique=True, null=False)
    country_name = models.CharField(max_length=100, null=False)
    country_name_jp = models.CharField(max_length=100, null=False)
    zone = models.CharField(max_length=1, null=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)

    class Meta:
        db_table = 'm_countries'

    def __str__(self):
        return f"{self.country_code} - {self.country_name}"

class Shipping(models.Model):
    zone = models.CharField(max_length=1, null=False)
    weight = models.IntegerField(null=False)
    basic_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)

    class Meta:
        db_table = 'm_shipping'

    def __str__(self):
        return f"Zone {self.zone} - {self.weight}kg"

class ShippingSurcharge(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    surcharge_type = models.CharField(max_length=50, null=False)  # 'FUEL', 'OVERSIZE', 'SATURDAY' など
    rate = models.DecimalField(max_digits=5, decimal_places=2, null=False)  # 割合（%）
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # 固定金額（ある場合）
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)  # nullの場合は現在有効

    class Meta:
        db_table = 'm_shipping_surcharge'

    def __str__(self):
        return f"{self.service.service_name} - {self.surcharge_type}" 

class EbayStoreType(models.Model):
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
    rate = models.DecimalField(max_digits=4, decimal_places=2, null=False)

    class Meta:
        db_table = 'm_tax'

    def __str__(self):
        return f"{self.rate}%"

class Setting(models.Model):
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
    status_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'm_status'

    def __str__(self):
        return self.status_name

class Condition(models.Model):
    condition_id = models.IntegerField(null=False)
    condition_enum = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'm_condition'

    def __str__(self):
        return f"{self.condition_id} - {self.condition_enum}"

class YahooAuctionStatus(models.Model):
    status_name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'm_yahoo_auction_status'

    def __str__(self):
        return self.status_name