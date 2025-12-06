from django.db.models import IntegerChoices, TextChoices


class HttpMethodChoices(TextChoices):
    GET = "GET", "GET"
    POST = "POST", "POST"
    PUT = "PUT", "PUT"
    PATCH = "PATCH", "PATCH"
    DELETE = "DELETE", "DELETE"


class EnvironmentChoices(TextChoices):
    DEV = "development", "DEVELOPMENT"
    PROD = "production", "PRODUCTION"
    STAGING = "staging", "STAGING"
