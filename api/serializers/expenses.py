from rest_framework import serializers
from api.models import Expense


class ExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = [
            'id', 'transaction_date', 'product_name', 'detail', 'price', 'tax', 'total_amount',
            'shipping_cost', 'client_name', 'client_company_name', 'client_postal_code',
            'client_address', 'url', 'insert_datetime', 'update_datetime'
        ]
        read_only_fields = ['id', 'insert_datetime', 'update_datetime']
