from django.urls import path

from .views import main, test

app_name = "exchange_rate"

urlpatterns = [
    path("", main, name="main"),
    path("test/", test, name="test"),

]
