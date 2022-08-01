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

    RABBIT_MQ_URL: SecretStr

    REDIS_URL: SecretStr
    REDIS_PORT: int

    AWS_ACCESS_KEY_ID: SecretStr
    AWS_SECRET_ACCESS_KEY: SecretStr

    KAKAO_LOGIN_REST_KEY: SecretStr

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env = Env()

SECRET_KEY = env.SECRET_KEY.get_secret_value()

DEBUG = False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "django_celery_beat",
    "django_celery_results",
]

MIDDLEWARE += []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.DB_HOST,
        "USER": env.DB_USERNAME,
        "PASSWORD": env.DB_PASSWORD.get_secret_value(),
        "NAME": env.DB_NAME,
    }
}

STATIC_URL = "/static/"

TIME_ZONE = env.TIME_ZONE

EXCHANGE_RATE_API_URL = env.EXCHANGE_RATE_API_URL

# celery
CELERY_ALWAYS_EAGER = True
# CELERY_BROKER_URL = 'amqp://[user_name]:[password]@localhost/[vhost_name]'
CELERY_BROKER_URL = env.RABBIT_MQ_URL.get_secret_value()
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = env.TIME_ZONE

# kakao login
KAKAO_LOGIN_REST_KEY = env.KAKAO_LOGIN_REST_KEY.get_secret_value()
KAKAO_LOGIN_REDIRECT_URL = "http://127.0.0.1:8000/account/login/kakao/callback/"

# channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(env.REDIS_URL.get_secret_value(), env.REDIS_PORT)],
        },
    },
}

# aws s3
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

AWS_ACCESS_KEY_ID = env.AWS_ACCESS_KEY_ID.get_secret_value()
AWS_SECRET_ACCESS_KEY = env.AWS_SECRET_ACCESS_KEY.get_secret_value()
AWS_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = "s3-exchange-rate"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com"
# 파일 캐시 유지 시간
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

# 같은 파일이 들어오면 덮어 쓰지 말라는 의미
AWS_S3_FILE_OVERWRITE = False
# 외부 접근 허용
AWS_DEFAULT_ACL = "public-read"

AWS_LOCATION = "static"

# AWS S3 사용을 위해 수정
STATIC_URL = f"http://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
