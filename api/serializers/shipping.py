from rest_framework import serializers
from ..models.master import (
    CountriesFedex,
    CountriesDhl,
    CountriesEconomy
)

class CountrySerializer(serializers.ModelSerializer):
    """国情報のシリアライザ"""
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = CountriesFedex
        fields = ['code', 'name']
    
    def get_name(self, obj):
        return obj.name_ja

class ShippingCalculatorRequestSerializer(serializers.Serializer):
    """送料計算リクエストのシリアライザ"""
    country_code = serializers.CharField(max_length=2, required=True)
    weight = serializers.FloatField(required=True)
    length = serializers.IntegerField(required=False, default=0)
    width = serializers.IntegerField(required=False, default=0)
    height = serializers.IntegerField(required=False, default=0)
    is_document = serializers.BooleanField(required=False, default=False)
    
    def validate_weight(self, value):
        try:
            # 文字列で来た場合にフロート変換を試みる
            weight_value = float(value)
            if weight_value <= 0:
                raise serializers.ValidationError("重量は0より大きい値を入力してください")
            return weight_value
        except (ValueError, TypeError):
            raise serializers.ValidationError("重量は有効な数値を入力してください")
    
    def validate(self, data):
        if 'length' in data and 'width' in data and 'height' in data:
            if data.get('length', 0) < 0 or data.get('width', 0) < 0 or data.get('height', 0) < 0:
                raise serializers.ValidationError("寸法には0以上の値を入力してください")
        return data

class ShippingRateResponseSerializer(serializers.Serializer):
    """送料計算結果のシリアライザ"""
    country = CountrySerializer()
    physical_weight = serializers.FloatField()
    weights_used = serializers.DictField(child=serializers.FloatField())
    shipping_rates = serializers.DictField(child=serializers.IntegerField())
    recommended_service = serializers.CharField() 