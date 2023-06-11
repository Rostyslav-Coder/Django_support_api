"""This is serializer module"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    """User seriflizer private class"""

    email = serializers.EmailField()
    password = serializers.CharField()


class UserPublicSerializer(serializers.ModelSerializer):
    """User seriflizer public class"""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
