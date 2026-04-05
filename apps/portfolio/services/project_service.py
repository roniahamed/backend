from django.db.models import Count, QuerySet

from apps.portfolio.models import Project, Service


def get_public_services_queryset() -> QuerySet[Service]:
    return (
        Service.objects.filter(is_active=True)
        .only(
            "id",
            "slug",
            "title",
            "summary",
            "long_description",
            "icon_key",
            "features",
            "tech_stack",
            "challenges_vs_solutions",
            "my_services",
            "development_process",
            "sort_order",
        )
        .prefetch_related("links__content_type")
        .order_by("sort_order", "title")
    )


def get_public_projects_queryset() -> QuerySet[Project]:
    # why: list and detail serializers both touch related images/metrics/links; prefetch stops N+1 explosions.
    return (
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
            "challenges",
            "solutions",
            "feature_items",
            "technical_architecture",
            "impact_metrics",
            "is_open_source",
            "thumbnail_image_url",
            "is_featured",
            "published_at",
        )
        .prefetch_related("images", "metrics", "links__content_type")
        .order_by("-published_at", "title")
    )
