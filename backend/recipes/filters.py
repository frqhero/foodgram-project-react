from django_filters import rest_framework as filters

from .models import Recipe

class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = Recipe
        fields = ['tags']

filters.FilterSet
# class RecipeFilter(django_filters.FilterSet):
#     author = django_filters.NumberFilter(field_name='author__id')
#     tags = django_filters.CharFilter(field_name='tags__slug')
#
#     class Meta:
#         model = Recipe
#         fields = ['author', 'tags']
