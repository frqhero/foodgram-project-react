from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from .models import Ingredient
from .serializers import IngredientSerializer
from rest_framework.filters import SearchFilter


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
