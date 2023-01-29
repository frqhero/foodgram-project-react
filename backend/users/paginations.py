from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    def get_page_size(self, request):
        page_size = request.query_params.get('limit', self.page_size)
        if page_size is not None:
            self.page_size = page_size
        return super().get_page_size(request)
