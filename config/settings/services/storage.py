from config.settings.packages.libs import INSTALLED_APPS
from config.settings.integrations_config import S3StorageConfig, BASE_DOMAIN, PROJECT_NAME


INSTALLED_APPS.append("storages")

AWS_ACCESS_KEY_ID = S3StorageConfig.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = S3StorageConfig.AWS_SECRET_ACCESS_KEY
AWS_S3_ENDPOINT_URL = S3StorageConfig.AWS_S3_ENDPOINT_URL
AWS_S3_FILE_OVERWRITE = True


# Base storage options
default_storage_options = {
    "bucket_name": S3StorageConfig.STORAGE_BUCKET_NAME,
    "location": "media",
}

staticfiles_storage_options = {
    "bucket_name": S3StorageConfig.STORAGE_BUCKET_NAME,
    "location": "static",
}

if S3StorageConfig.is_production() or S3StorageConfig.is_staging():
    default_storage_options["custom_domain"] = f"{BASE_DOMAIN}/{PROJECT_NAME}"
    staticfiles_storage_options["custom_domain"] = f"{BASE_DOMAIN}/{PROJECT_NAME}"

STORAGES = {
    "default": {  # MEDIA
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": default_storage_options,
    },
    "staticfiles": {  # STATIC
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": staticfiles_storage_options,
    },
}

if S3StorageConfig.is_development():
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
