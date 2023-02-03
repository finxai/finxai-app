from django.shortcuts import render
from .models import Stock
from .serializers import StockSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["GET"])
def stocks_list(request):
    if request.method == "GET":
        stocks = Stock.objects.order_by("ticker")

        if tickers := request.GET.get("tickers") or None:
            tickers = tickers.upper().split(",")
            stocks = stocks.filter(ticker__in=tickers)

        if exchange := request.GET.get("exchange") or None:
            exchange = exchange.upper()
            stocks = stocks.filter(exchange=exchange)

        if etf := request.GET.get("etf") or None:
            if etf == "yes":
                stocks = stocks.filter(is_etf=True)
            else:
                stocks = stocks.filter(is_etf=False)

        serializers = StockSerializers(stocks, many=True)
        return Response(serializers.data)
