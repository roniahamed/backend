from django.contrib import admin
from django.urls import include, path

from apps.core.views import HealthCheckView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", HealthCheckView.as_view(), name="public-health-check"),
    path("api/v1/", include("config.api_urls")),
]
