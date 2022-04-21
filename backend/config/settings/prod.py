from .settings import *
from pydantic import BaseSettings, SecretStr
from celery.schedules import crontab


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
        env_file = ".env"
        env_file_encoding = "utf-8"


env = Env()

SECRET_KEY = env.SECRET_KEY.get_secret_value()

DEBUG = False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    'django_celery_beat',
    'django_celery_results',
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
# CELERY_BROKER_URL = 'amqp://[user_name]:[password]@localhost/[vhost_name]'
CELERY_BROKER_URL = env.CELERY_BROKER_URL.get_secret_value()
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = env.TIME_ZONE

CELERY_BEAT_SCHEDULE = {
	# 9:00 ~ 15:00
	'update_exchange_rate': {
		'task': 'exchange_rate.tasks.update_exchange_rate',
		'schedule': crontab(hour='9-15', minute='*/5', day_of_week='1-5'),
	},
	# 15:00 ~ 15:30
	'end_update_exchange_rate': {
		'task': 'exchange_rate.tasks.update_exchange_rate',
		'schedule': crontab(hour='15', minute='0-30/5', day_of_week='1-5'),
	},
}