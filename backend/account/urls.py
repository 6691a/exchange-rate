from django.urls import path
from .views import kakao_login, kakao_logout, kakao_login_callback, login

app_name = "account"
urlpatterns = [
    path("login/", login, name="login"),

    path("kakao/login/", kakao_login, name="kakao_login"),
    path("logout/", kakao_logout, name="logout"),
    path("login/kakao/callback/", kakao_login_callback, name="kakao_login_callback"),
]
