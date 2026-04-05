from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class DefaultPageNumberPagination(PageNumberPagination):
    # why: Use env-backed settings so pagination tuning does not require deploy-time code edits.
    page_size = settings.API_DEFAULT_PAGE_SIZE
    page_size_query_param = "page_size"
    max_page_size = settings.API_MAX_PAGE_SIZE

