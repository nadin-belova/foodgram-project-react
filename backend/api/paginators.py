from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """
    Класс для настройки пагинации с
    фиксированным количеством элементов на странице.
    """

    page_size = 6
    page_size_query_param = "limit"
