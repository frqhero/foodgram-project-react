from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Recipe, RecipeIngredient
from users.serializers import MyDjoserUserCreateSerializer
from tags.serializers import TagSerializer
from ingredients.models import Ingredient
# from ingredients.serializers import IngredientSerializer


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'recipe', 'quantity']


class RecipeSerializer(ModelSerializer):
    author = MyDjoserUserCreateSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set')

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'ingredients', 'author', 'name']
        # depth = 1
