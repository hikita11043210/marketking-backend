from django.db import models
from django.conf import settings
class Expense(models.Model):
    """経費台帳テーブル"""
    transaction_date = models.DateField(null=False)
    product_name = models.TextField(null=False)
    detail = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    client_name = models.CharField(max_length=100, null=True, blank=True)
    client_company_name = models.CharField(max_length=100, null=True, blank=True)
    client_postal_code = models.CharField(max_length=100, null=True, blank=True)
    client_address = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    update_datetime = models.DateTimeField(auto_now=True)
    insert_datetime = models.DateTimeField(auto_now_add=True)
    insert_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='expense_insert_user')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='expense_update_user')
    class Meta:
        db_table = 't_expenses'

    def __str__(self):
        return f"{self.transaction_date} - {self.product_name}" 