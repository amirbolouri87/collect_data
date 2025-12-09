from config.settings.integrations_config import JWTConfig

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": JWTConfig.ACCESS_TOKEN_LIFETIME,
    "REFRESH_TOKEN_LIFETIME": JWTConfig.REFRESH_TOKEN_LIFETIME,
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
