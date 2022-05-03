from .settings import *
from pydantic import BaseSettings, SecretStr


class Env(BaseSettings):
    # DB
    DB_USERNAME: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # Django
    SECRET_KEY: SecretStr
    TIME_ZONE: str

    CELERY_BROKER_URL: SecretStr

    KAKAO_LOGIN_REST_KEY: SecretStr

    class Config:
        env_file = "dev.env"
        env_file_encoding = "utf-8"


env = Env()

SECRET_KEY = env.SECRET_KEY.get_secret_value()

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "django_celery_beat",
    "django_celery_results",
]

MIDDLEWARE += []


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "HOST": env.DB_HOST,
#         "USER": env.DB_USERNAME,
#         "PASSWORD": env.DB_PASSWORD.get_secret_value(),
#         "NAME": env.DB_NAME,
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"

TIME_ZONE = env.TIME_ZONE

KAKAO_LOGIN_REST_KEY = env.KAKAO_LOGIN_REST_KEY.get_secret_value()


ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_rabbitmq.core.RabbitmqChannelLayer",
        "CONFIG": {
            "host": env.CELERY_BROKER_URL.get_secret_value(),
        },
    },
}
