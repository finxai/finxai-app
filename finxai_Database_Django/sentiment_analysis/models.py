from django.db import models
from screener.models import Stock

# Create your models here.
class News(models.Model):
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="news")
    content = models.TextField()
    sentiment = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker.ticker
