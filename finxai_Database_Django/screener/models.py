from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=20, unique=True, primary_key=True)
    company_name = models.CharField(max_length=100)
    exchange = models.CharField(max_length=10)
    type = models.CharField(max_length=10, default="stock")
    is_etf = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker
