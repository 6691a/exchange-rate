from django.urls import path
from .views import kakao_login, kakao_logout, kakao_login_callback

app_name = "account"
urlpatterns = [
    path("login/", kakao_login, name="login"),
    path("logout/", kakao_logout, name="logout"),
    path("login/kakao/callback/", kakao_login_callback, name="kakao_login_callback"),
]
