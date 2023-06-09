"""URL configuration for config project."""

import hashlib
import json
import re
from functools import wraps

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from core.constants import Role
from core.models import User

# ****************************************************************************
# All roles are hardcoded instead of being used the database
# ****************************************************************************
ROLES = {
    "ADMIN": 1,
    "MANAGER": 2,
    "USER": 3,
}


def error_handler(func):
    """Decorator for error handling"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            message = {"error": str(error)}
            status_code = 400
        except Exception as error:
            message = {"error": str(error)}
            status_code = 500

        return HttpResponse(
            content_type="application/json",
            content=json.dumps(message),
            status=status_code,
        )

    return wrapper


@error_handler
def _get_user(request):
    username = request.GET.get("username")

    user = User.objects.get(username=username)  # pylint: disable=E1101
    response_data = {
        "username": user.username,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
    }

    return response_data


def _validate_email(email: str) -> None:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValueError("Email is not correct.")


def _hash_password(payload: str) -> str:
    return hashlib.md5(payload.encode()).hexdigest()


@error_handler
def _create_user(request):
    data = json.loads(request.body)

    _validate_email(data["email"])

    if User.objects.filter(  # pylint: disable=E1101
        username=data["username"], email=data["email"]
    ).exists():
        response_data = {"message": f"User {data['username']} already taken."}

        return response_data

    data["password"] = _hash_password(data["password"])
    data["role"] = Role.USER

    user = User.objects.create(  # pylint: disable=E1101
        username=data["userName"],
        email=data["email"],
        first_name=data["firstName"],
        last_name=data["lastName"],
        password=data["password"],
        role=data["role"],
    )

    response_data = {"message": f"User {user.username} created successfully."}

    return response_data


@error_handler
def _delete_user(request):
    """This funktion delete users from DB"""
    data = json.loads(request.body)
    username = data.get("username")

    user = User.objects.get(username=username)  # pylint: disable=E1101
    user.delete()
    response_data = {"message": f"User {username} delete successfully."}

    return response_data


@error_handler
def _update_user(request):
    data = json.loads(request.body)
    username = data.get("username")
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    user = User.objects.get(username=username)  # pylint: disable=E1101
    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    user.save()
    response_data = {"message": f"User {username} updated successfully."}

    return response_data


def _invalid_request():
    response_data = {"message": "Invalid request method."}

    return response_data


def user_view(request):
    """This function returns, creates and deletes users."""

    if request.method.upper() == "GET":
        response = _get_user(request)

    elif request.method.upper() == "POST":
        response = _create_user(request)

    elif request.method.upper() == "DELETE":
        response = _delete_user(request)

    elif request.method.upper() == "PUT":
        response = _update_user(request)

    else:
        response = _invalid_request()

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(response),
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", user_view),
]
