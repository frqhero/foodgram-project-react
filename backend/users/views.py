from rest_framework.viewsets import ModelViewSet
from users.models import User
from .serializers import UserSerializer
# from .permissions import AdminOnlyPermission


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (AdminOnlyPermission,)
