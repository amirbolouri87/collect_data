from ..core import *
from ..services import *
from ..packages import *

DEBUG = BaseConfig.DEBUG
ALLOWED_HOSTS = BaseConfig.ALLOWED_HOSTS

CELERY_BEAT_SCHEDULE = {
    "scrape-tgju-every-90s": {
        "task": "config.celery.scrape_tgju_table",
        "schedule": 30.0,
    },
}
