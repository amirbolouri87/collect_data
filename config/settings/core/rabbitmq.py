from config.settings.integrations_config import BaseConfig
from decouple import Config, RepositoryEnv

DEV_ENV_FILE = F".app_envs/{BaseConfig.ENVIRONMENT}/.rabbitmq_envs"
config = Config(RepositoryEnv(DEV_ENV_FILE))
RABBITMQ_HOST = config("RABBITMQ_HOST")
RABBITMQ_PORT = config("RABBITMQ_PORT")
RABBITMQ_USERNAME = config("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = config("RABBITMQ_PASSWORD")

