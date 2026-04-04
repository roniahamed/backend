from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.blog.models import BlogPost, Tag
from apps.blog.serializers import BlogPostDetailSerializer, BlogPostListSerializer, TagSerializer


@method_decorator(cache_page(60 * 5), name="dispatch")
class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	lookup_field = "slug"
	search_fields = ("title", "excerpt", "content", "tags__name")
	filterset_fields = ("tags__slug",)
	ordering_fields = ("published_at", "title")

	queryset = (
		BlogPost.objects.filter(status=BlogPost.STATUS_PUBLISHED)
		.select_related("author")
		.prefetch_related("tags")
		.only(
			"id",
			"slug",
			"title",
			"excerpt",
			"content",
			"cover_image_url",
			"published_at",
			"reading_time_minutes",
			"meta_description",
			"author_id",
		)
	)

	def get_serializer_class(self):
		if self.action == "retrieve":
			return BlogPostDetailSerializer
		return BlogPostListSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	serializer_class = TagSerializer
	pagination_class = None
	lookup_field = "slug"
	queryset = Tag.objects.all().order_by("name")
