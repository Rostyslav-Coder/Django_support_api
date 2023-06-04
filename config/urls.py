"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


import json
from functools import wraps

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from core.models import User

# ****************************************************************************
# All roles are hardcoded instead of being used the database
# ****************************************************************************
ROLES = {
    "ADMIN": 1,
    "MANAGER": 2,
    "USER": 3,
}


def error_handling(func):
    """Decorator for error handling"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except User.DoesNotExist:  # pylint: disable=E1101
            response_data = {"message": "User not found."}
            return response_data

    return wrapper


@error_handling
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


def _create_user(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    password = request.POST.get("password")

    if User.objects.filter(
        username=username, email=email
    ).exists():  # pylint: disable=E1101
        response_data = {"message": f"User {username} already taken."}

        return response_data

    user = User.objects.create(  # pylint: disable=E1101
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
        role=3,
    )

    response_data = {"message": f"User {user.username} created successfully."}

    return response_data


@error_handling
def _delete_user(request):
    """This funktion delete users from DB"""
    data = json.loads(request.body)
    username = data.get("username")

    user = User.objects.get(username=username)  # pylint: disable=E1101
    user.delete()
    response_data = {"message": f"User {username} delete successfully."}

    return response_data


@error_handling
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

    if request.method == "GET":
        response = _get_user(request)

    elif request.method == "POST":
        response = _create_user(request)

    elif request.method == "DELETE":
        response = _delete_user(request)

    elif request.method == "PUT":
        response = _update_user(request)

    else:
        response = _invalid_request()

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(response),
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("create-user/", user_view),
]
