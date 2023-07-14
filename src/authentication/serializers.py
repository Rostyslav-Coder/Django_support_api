"""This is module for configuration serializers in Authentication component."""

from rest_framework import serializers


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
