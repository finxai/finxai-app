from django.shortcuts import render
from .models import Stock
from rest_framework.response import Response
from .serializers import StockSerializers
from .serializers2 import Stock2Serializers
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Portfolio, Portfolio2


@api_view(['POST'])
def update(request):
    if request.method == "POST":
        ticker = request.POST.get("ticker") or None
        try:
            stock = Stock.objects.get(ticker=ticker.upper())
            date = request.POST.get("date") or None
            if ticker and date:

                instrument_universe = request.POST.get("instrument_universe") or None
                if instrument_universe:
                    instrument_universe = float(instrument_universe)

                index_examp = request.POST.get("index_examp") or None
                if index_examp:
                    index_examp = float(index_examp)

                defaults = {"instrument_universe": instrument_universe, "index_examp": index_examp}
                obj, created = Portfolio.objects.update_or_create(ticker=stock, date=date, defaults=defaults)
                return Response({"message": "Done for " + ticker}, status=status.HTTP_201_CREATED)
        except Stock.DoesNotExist:
            return Response({"error": "Not Found: " + ticker}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def port_weights_examp_update(request):
    if request.method == "POST":
        ticker = request.POST.get("ticker") or None
        try:
            stock = Stock.objects.get(ticker=ticker.upper())
            if ticker:

                port_weights_examp = request.POST.get("port_weights_examp") or None
                if port_weights_examp:
                    port_weights_examp = float(port_weights_examp)
                    defaults = {"port_weights_examp": port_weights_examp}
                    obj, created = Portfolio2.objects.update_or_create(ticker=stock, defaults=defaults)
                    return Response({"message": "Done for " + ticker}, status=status.HTTP_201_CREATED)
                return Response({"message": "Not done for " + ticker}, status=status.HTTP_400_BAD_REQUEST)
        except Stock.DoesNotExist:
            return Response({"error": "Not Found: " + ticker}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def detail(request):
    if request.method == "GET":
        ticker = request.GET.get("ticker") or "AAPL"
        if ticker:
            try:
                stock = Stock.objects.get(ticker=ticker.upper())
                serializers = StockSerializers(stock)
                return Response(serializers.data)
            except Stock.DoesNotExist:
                return Response({"error": "Not Found: " + ticker}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def port_weights_examp_detail(request):
    if request.method == "GET":
        ticker = request.GET.get("ticker") or "AAPL"
        if ticker:
            try:
                stock = Stock.objects.prefetch_related('portfolio2').get(ticker=ticker.upper())
                serializers = Stock2Serializers(stock)
                return Response(serializers.data)
            except Stock.DoesNotExist:
                return Response({"error": "Not Found: " + ticker}, status=status.HTTP_400_BAD_REQUEST)
