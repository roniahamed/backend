from django.urls import path

from apps.users.views import PublicProfileView

urlpatterns = [
    path("profile/", PublicProfileView.as_view(), name="public-profile"),
]
