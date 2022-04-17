from rest_framework import pagination
from rest_framework.response import Response


class ProductPagination(pagination.PageNumberPagination):
    page_size = 18

    def get_next_page_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_page_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_paginated_response(self, data, category):
        return Response({
            'category': {
                **category,
                'products': data,
                'prev_page_number': self.get_previous_page_number(),
                'next_page_number': self.get_next_page_number(),
            }
        })
