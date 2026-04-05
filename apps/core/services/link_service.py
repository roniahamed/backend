from django.db.models import QuerySet

from apps.core.models import Link


def get_active_links_queryset() -> QuerySet[Link]:
    return (
        Link.objects.filter(is_active=True)
        .select_related("content_type")
        .only(
            "id",
            "name",
            "url",
            "icon",
            "category",
            "sort_order",
            "is_active",
            "content_type_id",
            "object_id",
        )
    )
