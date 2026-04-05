import logging

import cloudinary.uploader
from celery import shared_task
from django.core.cache import cache

from apps.portfolio.models import Project

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 4},
    soft_time_limit=45,
    time_limit=60,
)
def optimize_project_cover_task(self, project_id: int, public_id: str) -> None:
    idempotency_key = f"project-cover-optimize:{project_id}:{public_id}"
    if not cache.add(idempotency_key, "1", timeout=600):
        logger.info("Cover optimization already executed key=%s", idempotency_key)
        return

    project = Project.objects.filter(pk=project_id).only("id", "slug").first()
    if project is None:
        logger.warning("Project not found for optimization id=%s", project_id)
        return

    # why: Cloudinary eager transforms offload image processing away from API workers.
    cloudinary.uploader.explicit(
        public_id,
        type="upload",
        eager=[
            {"width": 1280, "crop": "limit", "quality": "auto", "fetch_format": "auto"},
            {"width": 640, "height": 360, "crop": "fill", "gravity": "auto", "quality": "auto"},
        ],
        eager_async=False,
    )
    logger.info("Cover optimization completed project=%s public_id=%s", project.slug, public_id)
