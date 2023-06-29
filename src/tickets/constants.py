"""This is module for keeping constants in Ticket component."""

from enum import IntEnum


class TicketStatus(IntEnum):
    """Class that defines user roles."""

    NOT_STARTED = 1
    IN_PROGRESS = 2
    CLOSED = 3
