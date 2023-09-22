from rest_framework.pagination import BasePagination

class CustomPagination(BasePagination):
    page_size = 15