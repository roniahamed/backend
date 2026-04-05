from django.db.models import F, QuerySet

from apps.blog.models import BlogPost, Tag


def get_published_posts_queryset() -> QuerySet[BlogPost]:
    return (
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
        .order_by("-published_at")
    )


def increment_post_view_count(*, post_id: int) -> None:
    # why: F expression keeps increments atomic under concurrent traffic.
    BlogPost.objects.filter(pk=post_id).update(view_count=F("view_count") + 1)


def get_tags_queryset() -> QuerySet[Tag]:
    return Tag.objects.only("id", "name", "slug").order_by("name")
