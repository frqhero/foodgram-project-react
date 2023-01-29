from rest_framework.viewsets import ModelViewSet
from users.models import User
from .serializers import UserSerializer
from djoser.views import UserViewSet as DjoserUserViewSet
from .paginations import CustomPageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (AdminOnlyPermission,)


class MyViewSet(DjoserUserViewSet):
    pagination_class = CustomPageNumberPagination
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [IsAuthenticatedOrReadOnly]
            return [permission() for permission in self.permission_classes]
        else:
            return super().get_permissions()



