from datetime import timedelta
from decouple import config
from pathlib import Path
from shared.enums import EnvironmentChoices

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_NAME = "ew"
BASE_DOMAIN = ""


if (
    config("ENVIRONMENT", cast=str, default=EnvironmentChoices.DEV).lower() == EnvironmentChoices.DEV
):
    from decouple import Config, RepositoryEnv

    DEV_ENV_FILE = ".app_envs/development/.env"
    config = Config(RepositoryEnv(DEV_ENV_FILE))


class BaseConfig:
    BASE_DIR = BASE_DIR
    ENVIRONMENT = config("ENVIRONMENT", default=EnvironmentChoices.DEV).lower()
    DEBUG = config("DEBUG", cast=bool, default=False)
    ALLOWED_HOSTS = config(
        "ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")]
    )

    @classmethod
    def is_development(cls):
        return cls.ENVIRONMENT == EnvironmentChoices.DEV

    @classmethod
    def is_production(cls):
        return cls.ENVIRONMENT == EnvironmentChoices.PROD

    @classmethod
    def is_staging(cls):
        return cls.ENVIRONMENT == EnvironmentChoices.STAGING


class SecurityConfig(BaseConfig):
    SECRET_KEY = config("SECRET_KEY", cast=str)
    CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS", cast=bool, default=True)


class S3StorageConfig(BaseConfig):
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL")
    STORAGE_BUCKET_NAME = config("STORAGE_BUCKET_NAME")


class DataBaseConfig(BaseConfig):
    MAIN_DATABASE_ENGINE = config("MAIN_DATABASE_ENGINE")
    MAIN_DATABASE_NAME = config("MAIN_DATABASE_NAME")
    MAIN_DATABASE_USER = config("MAIN_DATABASE_USER")
    MAIN_DATABASE_PASSWORD = config("MAIN_DATABASE_PASSWORD")
    MAIN_DATABASE_HOST = config("MAIN_DATABASE_HOST")
    MAIN_DATABASE_PORT = config("MAIN_DATABASE_PORT", cast=int, default=5432)


class SentryConfig(BaseConfig):
    if BaseConfig.is_production():
        SENTRY_DSN = config("SENTRY_DSN")
        TRACES_SAMPLE_RATE = config("TRACES_SAMPLE_RATE", cast=float)


class JWTConfig(BaseConfig):
    ACCESS_TOKEN_LIFETIME = timedelta(seconds=config("ACCESS_TOKEN_LIFETIME", cast=int, default=600))
    REFRESH_TOKEN_LIFETIME = timedelta(seconds=config("REFRESH_TOKEN_LIFETIME", cast=int, default=3600))


class GunicornConfig(BaseConfig):
    GUNICORN_TIMEOUT = config("GUNICORN_TIMEOUT", cast=int, default=300)
    GUNICORN_HOST = config("GUNICORN_HOST", default="0.0.0.0")
    GUNICORN_PORT = config("GUNICORN_PORT", cast=int, default=8000)
