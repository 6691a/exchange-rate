from django.urls import path

from .views import currency, main

app_name = "exchange_rate"

urlpatterns = [
    path("", main, name="main"),

    path("<str:currency>", currency, name="currency"),

]
