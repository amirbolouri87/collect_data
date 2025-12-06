from config.settings.integrations_config import BaseConfig

# ############################### #
#      INTERNATIONALIZATION       #
# ############################### #
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [str(BaseConfig.BASE_DIR / "locale")]

LANGUAGE_CODE = "fa-IR"
LANGUAGES = (
    ("en", "English"),
    ("fa", "Persian"),
)
