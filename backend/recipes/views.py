from rest_framework.viewsets import ModelViewSet
from .models import Recipe, RecipeIngredient
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RecipeReadSerializer, RecipeCreateSerializer
from users.paginations import CustomPageNumberPagination
from .filters import RecipeFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAuthor


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeReadSerializer
        elif self.action == 'create' or self.action == 'partial_update':
            return RecipeCreateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'partial_update' or self.action == 'destroy':
            self.permission_classes = [IsAuthor]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.delete()
