from rest_framework.pagination import LimitOffsetPagination


class StandardSizePagination(LimitOffsetPagination):
    """
    Can use this pagination class when the API response will be smaller
    """

    default_limit: int = 10


class LargeSizePagination(LimitOffsetPagination):
    """
    Can use this pagination class when the API response will be larger
    """

    default_limit: int = 5
