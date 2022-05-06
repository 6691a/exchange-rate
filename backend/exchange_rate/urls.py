from django.urls import path

from .views import main, channels

app_name = "exchange_rate"
urlpatterns = [
    path("", main, name="main"),
    path("1/", channels, name="channels"),
]
