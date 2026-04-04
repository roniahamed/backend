from django.urls import path

from apps.core.views import ContactSubmissionCreateView, HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("contact/", ContactSubmissionCreateView.as_view(), name="contact-create"),
]
