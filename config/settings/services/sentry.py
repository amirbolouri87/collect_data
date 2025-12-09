from config.settings.integrations_config import SentryConfig


if SentryConfig.is_production():

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SentryConfig.SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=SentryConfig.TRACES_SAMPLE_RATE,
        send_default_pii=True,
    )
