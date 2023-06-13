"""API configuration for create Users, Reequests & Messages."""

import json

from django.contrib.auth import authenticate
from django.http import JsonResponse

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

    print(request.body)
    user_create_serializer = UserCreateRequestSerializer(
        data=json.loads(request.body)
    )
    user_create_serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**user_create_serializer.validated_data)

    user_public_serializer = UserCreateResponseSerializer(user)

    return JsonResponse(user_public_serializer.data)


# @base_error_handler
def login_user(request):
    if request.method != "POST":
        raise ValueError("Only POST method is allowed")

    print(request.body)
    user_login_serializer = LoginRequestSerializer(
        data=json.loads(request.body)
    )

    user_login_serializer.is_valid(raise_exception=True)

    email = user_login_serializer.validated_data["email"]
    password = user_login_serializer.validated_data["password"]

    user = authenticate(email=email, password=password)

    if user is not None:
        response_serializer = LoginResponseSerializer(user)
        return JsonResponse(response_serializer.data)

    raise Exception("Invalid Email or Password")
