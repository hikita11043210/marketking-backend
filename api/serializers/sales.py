from rest_framework import serializers
from api.models import Sales


class SalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sales
        fields = [
            'id', 'transaction_date', 'product_name', 'management_code', 'url', 'identification_type',
            'identification_number', 'quantity', 'price', 'import_tax', 'final_value_fee', 'international_fee',
            'tax', 'total_amount', 'shipping_cost', 'client_name', 'client_company_name', 'client_postal_code',
            'client_address', 'client_occupation', 'client_age', 'insert_datetime', 'update_datetime'
        ]
        read_only_fields = ['id', 'insert_datetime', 'update_datetime']
