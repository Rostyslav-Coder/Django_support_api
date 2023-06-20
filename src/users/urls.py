"""URL configuration for user."""

from django.urls import path

from users.api import UserCreateAPIView

urlpatterns = [path("create/", UserCreateAPIView.as_view())]  # type: ignore
