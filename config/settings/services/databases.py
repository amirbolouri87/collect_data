from config.settings.integrations_config import DataBaseConfig


DATABASES = {
    "default": {
        "ENGINE": DataBaseConfig.MAIN_DATABASE_ENGINE,
        "NAME": DataBaseConfig.MAIN_DATABASE_NAME,
        "USER": DataBaseConfig.MAIN_DATABASE_USER,
        "PASSWORD": DataBaseConfig.MAIN_DATABASE_PASSWORD,
        "HOST": DataBaseConfig.MAIN_DATABASE_HOST,
        "PORT": DataBaseConfig.MAIN_DATABASE_PORT,
        "OPTIONS": {"threaded": True},
    },
}
