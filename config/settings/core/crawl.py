from config.settings.integrations_config import BaseConfig
from decouple import Config, RepositoryEnv

DEV_ENV_FILE = F".app_envs/{BaseConfig.ENVIRONMENT}/.crawl_envs"
config = Config(RepositoryEnv(DEV_ENV_FILE))
COMBINED_CRAWL_URL = config("COMBINED_CRAWL_URL")

