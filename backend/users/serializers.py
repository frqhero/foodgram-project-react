from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class MyDjoserUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(allow_blank=False, max_length=150)
    last_name = serializers.CharField(allow_blank=False, max_length=150)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
