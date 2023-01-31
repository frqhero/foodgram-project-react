from djoser.views import UserViewSet as DjoserUserViewSet
from .paginations import CustomPageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class MyViewSet(DjoserUserViewSet):
    pagination_class = CustomPageNumberPagination

    # def get_permissions(self):
    #     if self.action == "list":
    #         self.permission_classes = [IsAuthenticatedOrReadOnly]
    #         return [permission() for permission in self.permission_classes]
    #     else:
    #         return super().get_permissions()
    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [IsAuthenticated]
            return [permission() for permission in self.permission_classes]
        else:
            return super().get_permissions()