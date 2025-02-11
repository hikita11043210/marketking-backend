from django.db import models
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
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        db_table = 'm_countries'

    def __str__(self):
        return f"{self.country_code} - {self.country_name}"

class Shipping(models.Model):
    zone = models.CharField(max_length=1, null=False)
    weight = models.IntegerField(null=False)
    basic_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        db_table = 'm_shipping'

    def __str__(self):
        return f"Zone {self.zone} - {self.weight}kg"

class ShippingSurcharge(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    surcharge_type = models.CharField(max_length=50, null=False)  # 'FUEL', 'OVERSIZE', 'SATURDAY' など
    rate = models.DecimalField(max_digits=5, decimal_places=2, null=False)  # 割合（%）
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # 固定金額（ある場合）
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)  # nullの場合は現在有効

    class Meta:
        db_table = 'm_shipping_surcharge'

    def __str__(self):
        return f"{self.service.service_name} - {self.surcharge_type}" 

class Setting(models.Model):
    yahoo_client_id = models.CharField(max_length=255, null=True, blank=True)
    yahoo_client_secret = models.CharField(max_length=255, null=True, blank=True)
    ebay_client_id = models.CharField(max_length=255, null=True, blank=True)
    ebay_dev_id = models.CharField(max_length=255, null=True, blank=True)
    ebay_client_secret = models.CharField(max_length=255, null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    deepl_api_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'm_setting'

    def __str__(self):
        return "Global Settings"

    @classmethod
    def get_settings(cls):
        """単一のグローバル設定を取得または作成する"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

    def save(self, *args, **kwargs):
        """常にIDを1として保存し、単一レコードを維持する"""
        self.pk = 1
        super().save(*args, **kwargs)