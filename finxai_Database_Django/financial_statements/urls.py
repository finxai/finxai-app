from django.urls import path
from .views import financials_list

urlpatterns = [path("financial-statements", financials_list, name="financials_list")]
