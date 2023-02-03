from rest_framework import serializers
from screener.models import Stock
from .models import Portfolio


class PortfolioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['date', 'instrument_universe', 'index_examp']


class StockSerializers(serializers.ModelSerializer):
    portfolio = PortfolioSerializers(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ["ticker", "company_name", "exchange", "type", "portfolio"]
