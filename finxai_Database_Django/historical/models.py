from django.db import models
from screener.models import Stock

# Create your models here.
class Price(models.Model):
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="prices")
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker.ticker
