from rest_framework.routers import DefaultRouter

from apps.portfolio.views import ProjectViewSet, ServiceViewSet

router = DefaultRouter()
router.register("services", ServiceViewSet, basename="service")
router.register("projects", ProjectViewSet, basename="project")

urlpatterns = router.urls
