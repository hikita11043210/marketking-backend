from rest_framework import serializers
from api.models import TransactionType, Transaction


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['id', 'value']
        read_only_fields = ['id']


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type_name = serializers.CharField(source='transaction_type.value', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_date', 'transaction_type', 'transaction_type_name',
            'product_name', 'management_code', 'url', 'identification_type', 'identification_number',
            'quantity', 'price', 'client_name', 'client_company_name', 'client_postal_code',
            'client_address', 'client_occupation', 'client_age', 'created_at', 'updated_at',
            'created_by', 'updated_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user.username
        validated_data['updated_by'] = user.username
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user.username
        return super().update(instance, validated_data) 