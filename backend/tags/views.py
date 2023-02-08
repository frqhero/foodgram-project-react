from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Tag
from .serializers import TagSerializer
from rest_framework.permissions import AllowAny


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
