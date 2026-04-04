from django.db.models import F
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.blog.models import BlogPost, Tag
from apps.blog.serializers import BlogPostDetailSerializer, BlogPostListSerializer, TagSerializer


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
			"view_count",
			"meta_description",
			"author_id",
		)
	)

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		# why: F-expression increments safely under concurrent reads.
		BlogPost.objects.filter(pk=instance.pk).update(view_count=F("view_count") + 1)
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
	queryset = Tag.objects.all().order_by("name")
