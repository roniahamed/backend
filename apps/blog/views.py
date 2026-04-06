from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.blog.serializers import BlogPostDetailSerializer, BlogPostListSerializer, TagSerializer
from apps.blog.services.blog_service import (
	get_published_posts_detail_queryset,
	get_published_posts_list_queryset,
	get_tags_queryset,
	increment_post_view_count,
)


@method_decorator(cache_page(60 * 5), name="dispatch")
class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	lookup_field = "slug"
	search_fields = ("title", "excerpt", "content", "tags__name")
	filterset_fields = ("tags__slug",)
	ordering_fields = ("published_at", "title")
	queryset = get_published_posts_list_queryset()

	def get_queryset(self):
		if self.action == "retrieve":
			return get_published_posts_detail_queryset()
		return get_published_posts_list_queryset()

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		increment_post_view_count(post_id=instance.pk)
		instance.refresh_from_db(fields=("view_count",))
		serializer = self.get_serializer(instance)
		return Response(serializer.data)

	def get_serializer_class(self):
		if self.action == "retrieve":
			return BlogPostDetailSerializer
		return BlogPostListSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	serializer_class = TagSerializer
	pagination_class = None
	lookup_field = "slug"
	queryset = get_tags_queryset()
