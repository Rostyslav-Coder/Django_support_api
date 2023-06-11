"""API configuration for create Users, Reequests & Messages."""

import json

from django.http import JsonResponse

from core.decorators import base_error_handler
from core.models import User
from core.serializers import UserCreateSerializer, UserPublicSerializer


@base_error_handler
def create_user(request):
    if request.method != "POST":
        raise ValueError("Only POST method is allowed")

    user_create_serializer = UserCreateSerializer(
        data=json.loads(request.body)
    )
    user_create_serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**user_create_serializer.validated_data)

    user_public_serializer = UserPublicSerializer(user)

    return JsonResponse(user_public_serializer.data)
