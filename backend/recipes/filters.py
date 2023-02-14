import django_filters
from .models import Recipe

class RecipeFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(field_name='author__id')
    tags = django_filters.CharFilter(field_name='tags__name')
    # is_favorited = django_filters.rest_framework.BooleanFilter(
    #     method='filter_is_favorited'
    # )

    def filter_is_favorited(self, qs, name, value):
        pass

    class Meta:
        model = Recipe
        fields = ['author', 'tags']