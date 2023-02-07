from rest_framework.viewsets import ModelViewSet
from .models import Recipe
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RecipeReadSerializer, RecipeCreateSerializer
from users.paginations import CustomPageNumberPagination
from .filters import RecipeFilter
from django_filters.rest_framework import DjangoFilterBackend


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeReadSerializer
        elif self.action == 'create':
            return RecipeCreateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
