from django.urls import path

from .consumers import ExchangeRateConsumer, WatchListConsumer

websocket_urlpatterns = [
    path("ws/exchange_rate/<str:currency>/", ExchangeRateConsumer.as_asgi()),
    path("ws/watch/<str:currency>/", WatchListConsumer.as_asgi()),

]
