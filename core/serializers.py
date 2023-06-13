"""This is serializer module"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateRequestSerializer(serializers.Serializer):
    """User request serializer class"""

    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)


class UserCreateResponseSerializer(serializers.ModelSerializer):
    """User response serializer class"""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class LoginRequestSerializer(serializers.Serializer):
    """Request Serializer to Login"""

    email = serializers.EmailField()
    password = serializers.CharField()


class LoginResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
