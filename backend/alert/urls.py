from django.urls import path

from .views import alert, alert_beat

app_name = "alert"

urlpatterns = [
    path("<str:currency>", alert, name="alert"),
    path("beat/<str:currency>", alert_beat, name="alert_beat"),

]
