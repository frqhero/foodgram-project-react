from rest_framework.viewsets import ModelViewSet
from .models import Recipe
from rest_framework.permissions import AllowAny
from .serializers import RecipeSerializer
from users.paginations import CustomPageNumberPagination
from .filters import RecipeFilter
from django_filters.rest_framework import DjangoFilterBackend

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
