from .fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from ingredients.models import Ingredient
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import DjoserUserCreateSerializer

from .models import Recipe, RecipeIngredient


class RecipeIngredientSerializer(ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ["id", "name", "measurement_unit", "amount"]


class RecipeReadSerializer(ModelSerializer):
    author = DjoserUserCreateSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True, source="recipeingredient_set"
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        ]

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        return obj.favorites.filter(pk=user.pk).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        return obj.purchases.filter(pk=user.pk).exists()


class RecipeIngredientForCreationSrl(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ["id", "amount"]


class RecipeCreateSerializer(ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Tag.objects.all(),
        allow_empty=False,
    )
    ingredients = RecipeIngredientForCreationSrl(many=True, allow_null=False)
    name = serializers.CharField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(min_value=1)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        ]

    def to_representation(self, instance):
        return RecipeReadSerializer(
            context={"request": self.context["request"]}
        ).to_representation(instance)

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                "At least one ingredient is required."
            )
        if len(set([x["id"] for x in value])) != len(value):
            raise serializers.ValidationError("Ingredients must be unique")
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        recipe = super().create(validated_data)
        self.create_recipe_ingredients(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop("ingredients")
        recipe = super().update(recipe, validated_data)
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        self.create_recipe_ingredients(recipe, ingredients)
        return recipe

    def create_recipe_ingredients(self, recipe, ingredients):
        new_entries = []
        for ingredient_initial_data in ingredients:
            new_recipe_ingredient = RecipeIngredient()
            new_recipe_ingredient.ingredient = ingredient_initial_data["id"]
            new_recipe_ingredient.recipe = recipe
            new_recipe_ingredient.amount = ingredient_initial_data["amount"]
            new_entries.append(new_recipe_ingredient)
        RecipeIngredient.objects.bulk_create(new_entries)


class RecipeFavSrl(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Recipe
        fields = ["id", "name", "image", "cooking_time"]
