from rest_framework import serializers

from apps.blog.models import BlogPost, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug")


class BlogPostListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = (
            "id",
            "slug",
            "title",
            "excerpt",
            "cover_image_url",
            "published_at",
            "reading_time_minutes",
            "view_count",
            "tags",
        )


class BlogPostDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = (
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
            "tags",
        )
