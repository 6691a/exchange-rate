from django.urls import re_path, path

from .consumers import ExchangeRateConsumer

websocket_urlpatterns = [
    path(r"ws/exchange_rate/", ExchangeRateConsumer.as_asgi()),
]
