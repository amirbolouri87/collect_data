"""
URL configuration for external_wrapper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from apps.health_check.api.v1.views.health_check import HealthCheckView
from config.settings.integrations_config import BaseConfig
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


simple_jwt_urlpatterns = [
    path(
        "account/api/v1/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("accounting/api/v1/verify/", TokenVerifyView.as_view(), name="verify"),
    path(
        "account/api/v1/login/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]


application_urlpatterns = [
    path("health/", view=HealthCheckView.as_view()),
]

admin_urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns = admin_urlpatterns + simple_jwt_urlpatterns + application_urlpatterns

if BaseConfig.is_production():
    urlpatterns.append(path("", include("django_prometheus.urls")))
