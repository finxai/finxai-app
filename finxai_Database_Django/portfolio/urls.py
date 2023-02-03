from django.urls import path
from .views import *

urlpatterns = [
    path("update", update, name="update"),
    path("detail", detail, name="detail"),
    path("port_weights_examp/update", port_weights_examp_update, name="port_weights_examp_update"),
    path("port_weights_examp/detail", port_weights_examp_detail, name="port_weights_examp_detail"),

]
