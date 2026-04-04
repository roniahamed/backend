from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.portfolio.models import Project, Service
from apps.portfolio.serializers import (
	ProjectDetailSerializer,
	ProjectListSerializer,
	ServiceSerializer,
)


@method_decorator(cache_page(60 * 5), name="dispatch")
class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	serializer_class = ServiceSerializer
	pagination_class = None
	lookup_field = "slug"
	queryset = Service.objects.filter(is_active=True).order_by("sort_order", "title")
	filterset_fields = ("is_active",)
	search_fields = ("title", "summary", "long_description")
	ordering_fields = ("sort_order", "title")


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	lookup_field = "slug"
	filterset_fields = ("category", "role", "is_featured")
	search_fields = ("title", "subtitle", "description", "abstract")
	ordering_fields = ("published_at", "title")

	# why: Preloading relations prevents N+1 on list/detail payloads.
	queryset = (
		Project.objects.filter(is_published=True)
		.annotate(image_count=Count("images", distinct=True))
		.only(
			"id",
			"slug",
			"title",
			"subtitle",
			"description",
			"abstract",
			"tech_stack",
			"user_roles",
			"security",
			"references",
			"period",
			"live_url",
			"github_url",
			"category",
			"role",
			"quote",
			"problem_statement",
			"thumbnail_image_url",
			"is_featured",
			"published_at",
		)
		.prefetch_related("images", "metrics")
		.order_by("-published_at", "title")
	)

	def get_serializer_class(self):
		if self.action == "retrieve":
			return ProjectDetailSerializer
		return ProjectListSerializer
