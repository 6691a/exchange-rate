from django.urls import path

from .views import main

app_name = "exchange_rate"
urlpatterns = [
    path("", main, name="main"),
]
