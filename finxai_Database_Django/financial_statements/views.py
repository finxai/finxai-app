from django.shortcuts import render
from .models import Stock
from .serializers import StockSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["GET"])
def financials_list(request):
    if request.method == "GET":
        ticker = request.GET.get("ticker") or None
        if ticker:
            try:
                stock= Stock.objects.get(ticker=ticker)
                serializers = StockSerializers(stock)
                return Response(serializers.data)
            except Stock.DoesNotExist:
                pass