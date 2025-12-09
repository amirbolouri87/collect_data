from config.settings.integrations_config import BaseConfig, PROJECT_NAME

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

if BaseConfig.is_production() or BaseConfig.is_staging():
    FORCE_SCRIPT_NAME = f"/{PROJECT_NAME}/"
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
