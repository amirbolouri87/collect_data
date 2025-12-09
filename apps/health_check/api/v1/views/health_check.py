import boto3
from botocore.exceptions import ClientError, EndpointConnectionError
from django.db import connections
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.integrations_config import  PROJECT_NAME
from django.conf import settings


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        checks = {
            "database": check_database(),
            # "storage": check_minio(),
            "sentry": check_sentry(),
            "prometheus": check_prometheus(),
        }

        # if S3StorageConfig.is_development() or S3StorageConfig.is_staging():
        #     relevant = ["database", "storage"]
        # else:
        relevant = list(checks.keys())

        is_healthy = all(checks[c] == "healthy" for c in relevant)

        return Response(
            {
                "service": PROJECT_NAME,
                # "environment": S3StorageConfig.ENVIRONMENT,
                "status": "healthy" if is_healthy else "unhealthy",
                "checks": checks,
            },
            status=status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE,
        )


def check_database():
    try:
        connections["default"].ensure_connection()
        return "healthy"
    except Exception:
        return "unhealthy"


def check_sentry():
    try:
        from sentry_sdk import Hub

        client = Hub.current.client
        return "healthy" if client and client.dsn else "not_configured"
    except ImportError:
        return "not_installed"
    except Exception:
        return "unhealthy"


_s3_client = None


# def check_minio():
#     global _s3_client
#     try:
#         if not _s3_client:
#             _s3_client = boto3.client(
#                 "s3",
#                 endpoint_url=S3StorageConfig.AWS_S3_ENDPOINT_URL,
#                 aws_access_key_id=S3StorageConfig.AWS_ACCESS_KEY_ID,
#                 aws_secret_access_key=S3StorageConfig.AWS_SECRET_ACCESS_KEY,
#             )
#         _s3_client.head_bucket(Bucket=S3StorageConfig.STORAGE_BUCKET_NAME)
#         return "healthy"
#     except EndpointConnectionError:
#         return "connection_failed"
#     except ClientError as e:
#         code = e.response.get("Error", {}).get("Code", "")
#         return "bucket_not_found" if code == "404" else "access_denied" if code == "403" else "unhealthy"
#     except Exception:
#         return "unhealthy"


def check_prometheus():
    if "django_prometheus" not in settings.INSTALLED_APPS:
        return "not_installed"

    try:
        from prometheus_client import REGISTRY
        list(REGISTRY.collect())
        return "healthy"
    except Exception:
        return "unhealthy"
