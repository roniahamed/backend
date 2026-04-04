from django.db.models import Count

from apps.blog.models import BlogPost
from apps.core.models import ContactSubmission
from apps.portfolio.models import Project, Service


def dashboard_callback(request, context):
    service_counts = list(
        Service.objects.values("is_active")
        .annotate(total=Count("id"))
        .order_by("is_active")
    )

    project_counts = list(
        Project.objects.values("is_open_source")
        .annotate(total=Count("id"))
        .order_by("is_open_source")
    )

    blog_popular = list(
        BlogPost.objects.filter(status=BlogPost.STATUS_PUBLISHED)
        .values("title", "view_count")
        .order_by("-view_count")[:5]
    )

    context.update(
        {
            "kpi_cards": {
                "projects": Project.objects.count(),
                "services": Service.objects.count(),
                "blogs": BlogPost.objects.count(),
                "contact_submissions": ContactSubmission.objects.count(),
            },
            "charts": {
                "service_counts": service_counts,
                "project_counts": project_counts,
            },
            "popular_blogs": blog_popular,
        }
    )

    return context
