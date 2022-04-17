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
<<<<<<< HEAD
    
    CELERY_BROKER_URL:str 
=======
>>>>>>> 082a1dc82938f28e80a03f9d0d9b40e4036d14de

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env = Env()

SECRET_KEY = env.SECRET_KEY.get_secret_value()

DEBUG = False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
<<<<<<< HEAD
    'django_celery_beat',
    'django_celery_results',
=======

>>>>>>> 082a1dc82938f28e80a03f9d0d9b40e4036d14de
]

MIDDLEWARE += [
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

EXCHANGE_RATE_API_URL = env.EXCHANGE_RATE_API_URL

# celery settings
CELERY_ALWAYS_EAGER = True
<<<<<<< HEAD
CELERY_BROKER_URL = env.CELERY_BROKER_URL
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = env.TIME_ZONE
=======
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = env.TIME_ZONE
>>>>>>> 082a1dc82938f28e80a03f9d0d9b40e4036d14de
