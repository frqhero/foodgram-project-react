from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser


User = get_user_model()


class MyDjoserUserCreateSerializer(UserCreateSerializer):
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
        if isinstance(user, AnonymousUser):
            return False
        return bool(user.subscriptions.filter(pk=obj.pk))