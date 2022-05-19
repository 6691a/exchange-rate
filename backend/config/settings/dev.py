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

    KAKAO_LOGIN_REST_KEY: SecretStr

    AWS_ACCESS_KEY_ID: SecretStr
    AWS_SECRET_ACCESS_KEY: SecretStr

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


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.DB_HOST,
        "USER": env.DB_USERNAME,
        "PASSWORD": env.DB_PASSWORD.get_secret_value(),
        "NAME": env.DB_NAME,
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# 해당 경로로 STATIC FILE 모임
# STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')

TIME_ZONE = env.TIME_ZONE

KAKAO_LOGIN_REST_KEY = env.KAKAO_LOGIN_REST_KEY.get_secret_value()

# channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {
        #     "hosts": [("127.0.0.1", 6379)],
        # },
    },
}

# # aws s3
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

# AWS_ACCESS_KEY_ID = env.AWS_ACCESS_KEY_ID.get_secret_value()
# AWS_SECRET_ACCESS_KEY = env.AWS_SECRET_ACCESS_KEY.get_secret_value()
# AWS_REGION = "ap-northeast-2"
# AWS_STORAGE_BUCKET_NAME = "s3-exchange-rate"
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com"
# # 파일 캐시 유지 시간
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": "max-age=86400",
# }

# # 같은 파일이 들어오면 덮어 쓰지 말라는 의미
# AWS_S3_FILE_OVERWRITE = False
# # 외부 접근 허용
# AWS_DEFAULT_ACL = "public-read"

# AWS_LOCATION = "static"

# # AWS S3 사용을 위해 수정
# STATIC_URL = f"http://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
