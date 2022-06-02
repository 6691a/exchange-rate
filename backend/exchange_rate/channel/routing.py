from django.urls import path

from .consumers import ExchangeRateConsumer, TestConsumer

websocket_urlpatterns = [
    path("ws/exchange_rate/<str:currency>/", ExchangeRateConsumer.as_asgi()),
    path("ws/test/", TestConsumer.as_asgi()),

]
