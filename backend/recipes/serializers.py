from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Recipe, RecipeIngredient
from users.serializers import MyDjoserUserCreateSerializer
from tags.serializers import TagSerializer


class RecipeIngredientSerializer(ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField (source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'quantity']


class RecipeSerializer(ModelSerializer):
    author = MyDjoserUserCreateSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set')

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'name']
