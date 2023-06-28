"""This is module for configuration app in Ticket component."""

from django.apps import AppConfig


class TicketsConfig(AppConfig):
    """A class that configurat Tickets."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "tickets"
