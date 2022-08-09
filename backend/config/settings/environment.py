
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
    SETTING_PATH: str

    # API URL
    EXCHANGE_RATE_API_URL: str
    KAKAO_LOGIN_REST_KEY: SecretStr

    # URLS
    RABBIT_MQ_URL: SecretStr
    REDIS_URL: SecretStr
    REDIS_PORT: int

    # AWS
    AWS_ACCESS_KEY_ID: SecretStr
    AWS_SECRET_ACCESS_KEY: SecretStr

    class Config:
        secrets_dir = "../"
        env_file = ".env"
        env_file_encoding = "utf-8"


ENV = Env()