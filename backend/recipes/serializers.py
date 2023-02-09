from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Recipe, RecipeIngredient
from users.serializers import MyDjoserUserCreateSerializer
from tags.serializers import TagSerializer
from tags.models import Tag
from ingredients.models import Ingredient
from django.core.files.base import ContentFile
import base64


class RecipeIngredientSerializer(ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')

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


class RecipeIngredientForCreationSrl(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeCreateSerializer(ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, read_only=False, queryset=Tag.objects.all(), allow_empty=False
    )
    ingredients = RecipeIngredientForCreationSrl(many=True, allow_null=False)
    name = serializers.CharField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(min_value=1)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['ingredients', 'tags', 'image', 'name', 'text', 'cooking_time']

    def to_representation(self, instance):
        return RecipeReadSerializer().to_representation(instance)

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError("At least one ingredient is required.")
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)
        new_entries = []
        for ingredient_initial_data in ingredients:
            new_recipe_ingredient = RecipeIngredient()
            new_recipe_ingredient.ingredient = ingredient_initial_data['id']
            new_recipe_ingredient.recipe = instance
            new_recipe_ingredient.amount = ingredient_initial_data['amount']
            new_entries.append(new_recipe_ingredient)
        RecipeIngredient.objects.bulk_create(new_entries)
        return instance

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        new_entries = []
        for ingredient_initial_data in ingredients:
            new_recipe_ingredient = RecipeIngredient()
            new_recipe_ingredient.ingredient = ingredient_initial_data['id']
            new_recipe_ingredient.recipe = instance
            new_recipe_ingredient.amount = ingredient_initial_data['amount']
            new_entries.append(new_recipe_ingredient)
        RecipeIngredient.objects.bulk_create(new_entries)
        return instance
