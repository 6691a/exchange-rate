from django.urls import path

from .consumers import ExchangeRateConsumer

websocket_urlpatterns = [
    path("ws/exchange_rate/<str:currency>/", ExchangeRateConsumer.as_asgi()),
]
