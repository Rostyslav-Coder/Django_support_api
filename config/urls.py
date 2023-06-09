"""URL configuration for config project."""

from django.contrib import admin
from django.urls import path

from core.api import user_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", user_view),
]
