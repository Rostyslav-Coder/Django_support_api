"""This is module for assign Manager to Ticket."""

from django.contrib.auth import get_user_model

from tickets.models import Ticket

User = get_user_model()


class AssignService:
    """This is c lass to assign Managers."""

    def __init__(self, ticket: Ticket):
        self._ticket = ticket

    def assign_manager(self, user: User):  # type: ignore
        """This is functin to assign Managers."""

        self._ticket.manager = user
        self._ticket.save()
