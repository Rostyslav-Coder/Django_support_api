"""This is Users Configuration module."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Class to create Users Configuration"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
