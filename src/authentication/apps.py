"""This is module for configuration app in Authentication component"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """User Authentication Configuration class"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
