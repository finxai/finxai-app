from rest_framework import serializers
from .models import Stock


class StockSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["ticker", "company_name", "exchange", "type"]
