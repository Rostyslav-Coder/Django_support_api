"""This is User Serializer module"""

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.constants import Role

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """User Registration Serializer class"""

    class Meta:
        """User Registration Serializer meta class"""

        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        attrs["password"] = make_password(attrs["password"])
        attrs["role"] = Role.USER

        return attrs


class UserPublicSerializer(serializers.ModelSerializer):
    """User response serializer class"""

    class Meta:
        """User Response Serializer meta class"""

        model = User
        fields = ["id", "email", "first_name", "last_name"]
