"""This is module to create Tickets & Messages DB Table with fields."""

from django.conf import settings
from django.db import models


class Ticket(models.Model):
    """Class to create Request Table"""

    title = models.CharField(max_length=100)
    text = models.TextField()
    visibility = models.BooleanField(default=True)
    status = models.PositiveSmallIntegerField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="user_tikets",
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="manager_tickets",
    )

    class Meta:
        """Class Meta to rename tickets table"""

        db_table = "tickets"


class Message(models.Model):
    """Class to create Message Table"""

    text = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="messages",
    )
    request = models.ForeignKey(
        "tickets.Ticket", on_delete=models.RESTRICT, related_name="messages"
    )

    class Meta:
        """Class Meta to rename message table"""

        db_table = "messages"
