from django.urls import path

from .views import exchange_rate, main

app_name = "exchange_rate"

urlpatterns = [
    path("", main, name="main"),

    # path("<str:currency>", exchange_rate, name="main"),
    # path("test/", test, name="test"),

]
