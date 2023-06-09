"""API configuration for create Users, Reequests & Messages."""

import hashlib
import json
import re
from functools import wraps

from django.http import JsonResponse

from core.constants import Role
from core.models import User


def error_handler(func):
    """Decorator for error handling"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            message = {"error": str(error)}
            status_code = 400
        except Exception as error:  # pylint: disable=W0718
            message = {"error": str(error)}
            status_code = 500

        return JsonResponse(
            data=message,
            status=status_code,
        )

    return wrapper


@error_handler
def _get_user(request):
    """This function returns users."""

    data = json.loads(request.body)

    user = User.objects.get(username=data["userName"])  # pylint: disable=E1101
    response_data = {
        "userName": user.username,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
    }

    return response_data


def _validate_email(email: str) -> None:
    """This function validate users email."""

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValueError("Email is not correct.")


def _hash_password(payload: str) -> str:
    """This function hashed users password."""

    return hashlib.md5(payload.encode()).hexdigest()


@error_handler
def _create_user(request):
    """This function creates users."""

    data = json.loads(request.body)

    _validate_email(data["email"])

    if User.objects.filter(  # pylint: disable=E1101
        username=data["userName"], email=data["email"]
    ).exists():
        response_data = {"message": f"User {data['userName']} already taken."}

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

    user = User.objects.get(username=data["userName"])  # pylint: disable=E1101
    user.delete()
    response_data = {
        "message": f"User {data['userName']} delete successfully."
    }

    return response_data


@error_handler
def _update_user(request):
    """This function updates users."""

    data = json.loads(request.body)

    user = User.objects.get(username=data["userName"])  # pylint: disable=E1101
    if data["email"]:
        user.email = data["email"]
    if data["firstName"]:
        user.first_name = data["firstName"]
    if data["lastName"]:
        user.last_name = data["lastName"]
    user.save()
    response_data = {
        "message": f"User {data['userName']} updated successfully."
    }

    return response_data


def _invalid_request():
    """This function return message if user, use invalid request method ."""

    response_data = {"message": "Invalid request method."}

    return response_data


def user_view(request):
    """This function returns, creates, deletes & updates users."""

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

    return JsonResponse(
        data=response,
    )
