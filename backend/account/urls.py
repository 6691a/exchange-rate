
from django.urls import path
from .views import kakao_login, login
urlpatterns = [
    path('login/', login, name="login"),
    #  path('login/kakao/callback/', kakao_login_callback, name="kakao_login_callback"),
]