from django_filters import rest_framework as filters

from .models import Recipe

class RecipeFilter(filters.FilterSet):
    author = filters.CharFilter(
        field_name='author__id'
    )

    class Meta:
        model = Recipe
        fields = ['author']
