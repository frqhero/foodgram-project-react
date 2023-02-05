from rest_framework.viewsets import ModelViewSet
from .models import Recipe
from rest_framework.permissions import AllowAny
from .serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RecipeSerializer
