from django.test import TestCase
from .models import User


def create_user(email: str) -> User:
    user = User.objects.create(
        email=email,
        nickname="user",
        gender="male",
        age_range="20~29",
        refresh_token="NULL",
    )
    user.set_password("1234")
    user.save()
    return user
