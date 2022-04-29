from django.urls import path
from .views import kakao_login, kakao_login_callback

urlpatterns = [
    path("login/", kakao_login, name="login"),
    path("login/kakao/callback/", kakao_login_callback, name="kakao_login_callback"),
]
