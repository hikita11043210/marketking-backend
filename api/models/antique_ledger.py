from django.db import models
from django.conf import settings
from .master import TransactionType

class Transaction(models.Model):
    """古物台帳テーブル"""
    transaction_date = models.DateField(null=False)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
    product_name = models.TextField(null=False)
    management_code = models.CharField(max_length=100, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    identification_type = models.CharField(max_length=50, null=True, blank=True)
    identification_number = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=False, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    client_name = models.CharField(max_length=100, null=True, blank=True)
    client_company_name = models.CharField(max_length=100, null=True, blank=True)
    client_postal_code = models.CharField(max_length=100, null=True, blank=True)
    client_address = models.TextField(null=True, blank=True)
    client_occupation = models.CharField(max_length=100, null=True, blank=True)
    client_age = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 't_transactions'

    def __str__(self):
        return f"{self.transaction_date} - {self.product_name}" 