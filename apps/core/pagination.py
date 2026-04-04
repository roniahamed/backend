from rest_framework.pagination import PageNumberPagination


class DefaultPageNumberPagination(PageNumberPagination):
    # why: Small pages protect DB and keep mobile payloads fast.
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 50
