from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.core.views import ContactSubmissionCreateView, HealthCheckView, LinkViewSet

router = DefaultRouter()
router.register("links", LinkViewSet, basename="link")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("contact/", ContactSubmissionCreateView.as_view(), name="contact-create"),
]

urlpatterns += router.urls
