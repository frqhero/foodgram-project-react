from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Recipe, RecipeIngredient
from users.serializers import MyDjoserUserCreateSerializer
from tags.serializers import TagSerializer
from tags.models import Tag


class RecipeIngredientSerializer(ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')
    amount = serializers.IntegerField(source='quantity')

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeReadSerializer(ModelSerializer):
    author = MyDjoserUserCreateSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set')

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time']


class RecipeCreateSerializer(ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ['ingredients', 'tags', 'image', 'name', 'text', 'cooking_time']

    def to_representation(self, instance):
        return RecipeReadSerializer().to_representation(instance)
