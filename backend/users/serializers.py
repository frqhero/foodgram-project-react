from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipe

User = get_user_model()


class DjoserUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(allow_blank=False, max_length=150)
    last_name = serializers.CharField(allow_blank=False, max_length=150)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_subscribed"
        )
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.subscriptions.filter(pk=obj.pk).exists()


class RecipeFavSrl(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class SubSrl(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeFavSrl(many=True, source='recipe_set')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            'recipes',
            'recipes_count'
        ]

    def get_is_subscribed(self, obj):
        return True
        """да, так просто, потому что этот сериализатор используется
        во вьюшке (в этом же приложении) кверисет у которой это
        юзеры на кого подписан юзер, поэтому если кверисет не пустой,
        то юзер полюбому на него подписан"""

    def get_recipes_count(self, obj):
        return obj.recipe_set.count()
