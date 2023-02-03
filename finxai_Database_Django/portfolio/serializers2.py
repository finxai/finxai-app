from rest_framework import serializers
from screener.models import Stock
from .models import Portfolio2


class Portfolio2Serializers(serializers.ModelSerializer):
    class Meta:
        model = Portfolio2
        fields = ['port_weights_examp']


class Stock2Serializers(serializers.ModelSerializer):
    portfolio2 = Portfolio2Serializers(many=True)

    class Meta:
        model = Stock
        fields = ["ticker", "company_name", "exchange", "type", "portfolio2"]
