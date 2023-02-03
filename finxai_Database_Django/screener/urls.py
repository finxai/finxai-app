from django.urls import path
from .views import stocks_list

urlpatterns = [path("stocks", stocks_list, name="stocks_list")]
