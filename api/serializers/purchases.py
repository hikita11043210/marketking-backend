from rest_framework import serializers
from api.models import Purchase


class PurchasesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = [
            'id', 'transaction_date', 'product_name', 'management_code', 'url', 'identification_type',
            'identification_number', 'quantity', 'price', 'tax', 'shipping_cost', 'total_amount',
            'invoice_number', 'client_name', 'client_company_name', 'client_postal_code',
            'client_address', 'client_occupation', 'client_age', 'insert_datetime', 'update_datetime'
        ]
        read_only_fields = ['id', 'insert_datetime', 'update_datetime']
