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

    ASGI_RABBIT_MQ_URL: SecretStr

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
STATICFILES_DIRS = [
    BASE_DIR / "static",
    # ("node", BASE_DIR / "node_modules"),
]

TIME_ZONE = env.TIME_ZONE

KAKAO_LOGIN_REST_KEY = env.KAKAO_LOGIN_REST_KEY.get_secret_value()

# channels
ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
