import logging

from celery import shared_task
from django.core.cache import cache
from django.db.models import Count

from apps.blog.models import BlogPost

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 2},
    soft_time_limit=30,
    time_limit=40,
)
def warm_blog_cache_task(self) -> None:
    # why: Pre-warming high-traffic list payload keeps first-byte latency predictable.
    top_posts = list(
        BlogPost.objects.filter(status=BlogPost.STATUS_PUBLISHED)
        .only("slug", "title", "published_at")
        .order_by("-published_at")[:20]
        .values("slug", "title", "published_at")
    )
    cache.set("blog:warm:list", top_posts, timeout=300)
    logger.info("Blog cache warmed posts=%s", len(top_posts))


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 2},
    soft_time_limit=30,
    time_limit=40,
)
def aggregate_tag_usage_task(self) -> None:
    usage = list(
        BlogPost.tags.through.objects.values("tag_id")
        .annotate(total=Count("tag_id"))
        .order_by("-total")[:50]
    )
    cache.set("blog:analytics:tag_usage", usage, timeout=600)
    logger.info("Tag analytics aggregated rows=%s", len(usage))
