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
    EXCHANGE_RATE_API_URL: str
    
    CELERY_BROKER_URL: SecretStr 

    class Config:
        env_file = "dev.env"
        env_file_encoding = "utf-8"



env = Env()

SECRET_KEY = env.SECRET_KEY.get_secret_value()

DEBUG = True

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS += [
]

MIDDLEWARE += [
    'django_celery_beat',
    'django_celery_results',
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.DB_HOST,
        "USER": env.DB_USERNAME,
        "PASSWORD": env.DB_PASSWORD.get_secret_value(),
        "NAME": env.DB_NAME,
    }
}

TIME_ZONE = env.TIME_ZONE

# celery settings
CELERY_ALWAYS_EAGER = True
# CELERY_BROKER_URL = 'amqp://[user_name]:[password]@localhost/[vhost_name]'
CELERY_BROKER_URL = env.CELERY_BROKER_URL.get_secret_value()
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = env.TIME_ZONE
