from django.urls import path

from .views import main, index, room

app_name = "exchange_rate"
urlpatterns = [
    path("", index, name="main"),
    path("<str:room_name>/", room, name="room"),
    # path("", main, name="main"),
]
