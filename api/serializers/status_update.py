from rest_framework import serializers
from api.models.yahoo import YahooAuction, YahooFreeMarket


class YahooAuctionStatusUpdateSerializer(serializers.ModelSerializer):
    """Yahooオークションのステータス更新用シリアライザ"""
    status_id = serializers.IntegerField()

    class Meta:
        model = YahooAuction
        fields = ['status_id']


class YahooFreeMarketStatusUpdateSerializer(serializers.ModelSerializer):
    """Yahooフリマのステータス更新用シリアライザ"""
    status_id = serializers.IntegerField()

    class Meta:
        model = YahooFreeMarket
        fields = ['status_id'] 