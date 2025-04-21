from rest_framework import serializers
from ..models.master import (
    ShippingRatesFedex,
    ShippingRatesDhl,
    ShippingRatesEconomy,
    CountriesFedex,
    CountriesDhl,
    CountriesEconomy
)

class ShippingRatesFedexSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRatesFedex
        fields = ['id', 'zone', 'weight', 'rate']

class ShippingRatesDhlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRatesDhl
        fields = ['id', 'zone', 'weight', 'is_document', 'rate']

class ShippingRatesEconomySerializer(serializers.ModelSerializer):
    country_code = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = ShippingRatesEconomy
        fields = ['id', 'country', 'weight', 'rate', 'country_code']
        read_only_fields = ['country']
    
    def create(self, validated_data):
        country_code = validated_data.pop('country_code', None)
        if country_code:
            country = CountriesEconomy.objects.get(code=country_code)
            validated_data['country'] = country
        return super().create(validated_data)

class CountriesFedexSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountriesFedex
        fields = ['id', 'code', 'name', 'zone', 'je_ip', 'je_ficp', 'ji_ip', 'ji_ficp'] 

class CountriesDhlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountriesDhl
        fields = ['id', 'code', 'name', 'zone', 'express_envelope', 'express_worldwide', 'express_worldwide_1200', 'express_worldwide_1030', 'express_worldwide_0900']

class CountriesEconomySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountriesEconomy
        fields = ['id', 'code', 'name', 'zone']
