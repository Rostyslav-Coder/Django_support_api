"""URL configuration for config project."""

from django.contrib import admin
from django.urls import path

from core.api import create_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", create_user),
]
