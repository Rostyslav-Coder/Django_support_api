"""This is module to creating Tickets & Message DB Tabl in Ticket component."""

from django.conf import settings
from django.db import models

from tickets.constants import TicketStatus


class Ticket(models.Model):
    """Class to create Ticket BD Table."""

    title = models.CharField(max_length=100)
    text = models.TextField()
    visibility = models.BooleanField(default=True)
    status = models.PositiveSmallIntegerField(default=TicketStatus.NOT_STARTED)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="user_tikets",
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="manager_tickets",
        null=True,
    )

    class Meta:
        """Class Meta to rename tickets table."""

        db_table = "tickets"


class Message(models.Model):
    """Class to create Message BD Table."""

    text = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="messages",
    )
    ticket = models.ForeignKey(
        "tickets.Ticket", on_delete=models.RESTRICT, related_name="messages"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Class Meta to rename message table."""

        db_table = "messages"
