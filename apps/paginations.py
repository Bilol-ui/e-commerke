from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    page_size = 6
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'current_page': self.page.number,
                'page_size': self.get_page_size(self.request),
                'total_items': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'results': data
        })
