"""API configuration for create Users, Reequests & Messages."""

import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from core.decorators import base_error_handler
from core.models import User
from core.serializers import (
    LoginRequestSerializer,
    LoginResponseSerializer,
    UserCreateRequestSerializer,
    UserCreateResponseSerializer,
)


@base_error_handler
def create_user(request):
    if request.method != "POST":
        raise ValueError("Only POST method is allowed")

    user_create_serializer = UserCreateRequestSerializer(
        data=json.loads(request.body)
    )
    user_create_serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**user_create_serializer.validated_data)

    user_public_serializer = UserCreateResponseSerializer(user)

    return JsonResponse(user_public_serializer.data)


@base_error_handler
def login_user(request):
    if request.method != "POST":
        raise ValueError("Only POST method is allowed")

    user_login_serializer = LoginRequestSerializer(
        data=json.loads(request.body)
    )
    user_login_serializer.is_valid(raise_exception=True)

    email = user_login_serializer["email"]
    password = user_login_serializer["password"]

    user = authenticate(email=email, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(  # pylint: disable=E1101
            user=user
        )
        response_serializer = LoginResponseSerializer(
            user, data={"token": token.key}
        )
        response_serializer.is_valid(raise_exception=True)
        return JsonResponse(response_serializer.data)

    raise AuthenticationFailed("Invalid Email or Password")
