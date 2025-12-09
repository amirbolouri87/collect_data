from config.settings.integrations_config import BaseConfig


if BaseConfig.is_production():
    from config.settings.core.middleware import MIDDLEWARE
    from config.settings.packages.libs import INSTALLED_APPS

    PROMETHEUS_MIDDLEWARES = [
        "django_prometheus.middleware.PrometheusBeforeMiddleware",
        "django_prometheus.middleware.PrometheusAfterMiddleware",
    ]
    INSTALLED_APPS.append("django_prometheus")
    MIDDLEWARE = [PROMETHEUS_MIDDLEWARES[0], *MIDDLEWARE, PROMETHEUS_MIDDLEWARES[1]]
