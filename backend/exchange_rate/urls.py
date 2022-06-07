from django.urls import path

from .views import exchange_rate, main, test

app_name = "exchange_rate"

urlpatterns = [
    path("", main),

    path("<str:currency>", exchange_rate, name="main"),
    path("test/", test, name="test"),

]
