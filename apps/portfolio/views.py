from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.portfolio.serializers import (
	ProjectDetailSerializer,
	ProjectListSerializer,
	ServiceSerializer,
)
from apps.portfolio.services.project_service import (
	get_public_projects_detail_queryset,
	get_public_projects_list_queryset,
	get_public_services_queryset,
)


@method_decorator(cache_page(60 * 5), name="dispatch")
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	serializer_class = ServiceSerializer
	pagination_class = None
	lookup_field = "slug"
	queryset = get_public_services_queryset()
	filterset_fields = ("is_active",)
	search_fields = ("title", "slug", "summary", "long_description")
	ordering_fields = ("sort_order", "title", "id")


@method_decorator(cache_page(60 * 5), name="dispatch")
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	lookup_field = "slug"
	filterset_fields = ("category", "role", "is_featured", "is_open_source")
	search_fields = ("title", "slug", "subtitle", "description", "abstract")
	ordering_fields = ("published_at", "title", "id")
	queryset = get_public_projects_list_queryset()

	def get_queryset(self):
		if self.action == "retrieve":
			return get_public_projects_detail_queryset()
		return get_public_projects_list_queryset()

	def get_serializer_class(self):
		if self.action == "retrieve":
			return ProjectDetailSerializer
		return ProjectListSerializer
