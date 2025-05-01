from rest_framework import serializers
from ..models.master import EbayStoreType

class EbayStoreTypeSerializer(serializers.ModelSerializer):
    """eBayストアタイプのシリアライザー"""
    class Meta:
        model = EbayStoreType
        fields = [
            'id',
            'store_type',
            'monthly_fee',
            'monthly_fee_annual',
            'free_listings',
            'listing_fee_over_limit',
            'final_value_fee',
            'final_value_fee_category_discount',
            'international_fee'
        ] 