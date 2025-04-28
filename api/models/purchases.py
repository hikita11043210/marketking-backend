from django.db import models
from .ebay import Ebay
class Purchase(models.Model):
    """仕入テーブル"""
    ebay_id = models.ForeignKey(Ebay, on_delete=models.CASCADE, null=True, blank=True)
    transaction_date = models.DateField(null=False)
    product_name = models.TextField(null=True)
    management_code = models.CharField(max_length=100, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    identification_type = models.CharField(max_length=50, null=True, blank=True)
    identification_number = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=False, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    invoice_number = models.CharField(max_length=100, null=True, blank=True)
    client_name = models.CharField(max_length=100, null=True, blank=True)
    client_company_name = models.CharField(max_length=100, null=True, blank=True)
    client_postal_code = models.CharField(max_length=100, null=True, blank=True)
    client_address = models.TextField(null=True, blank=True)
    client_occupation = models.CharField(max_length=100, null=True, blank=True)
    client_age = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    update_datetime = models.DateTimeField(auto_now=True)
    insert_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_purchases'

    def __str__(self):
        return f"{self.transaction_date} - {self.product_name}" 