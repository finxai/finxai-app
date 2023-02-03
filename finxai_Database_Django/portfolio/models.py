from django.db import models
from screener.models import Stock
# Create your models here.

class Portfolio(models.Model):
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="portfolio")
    date = models.DateField()
    instrument_universe = models.FloatField(null=True)
    index_examp = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker.ticker

class Portfolio2(models.Model):
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="portfolio2")
    port_weights_examp = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker.ticker

