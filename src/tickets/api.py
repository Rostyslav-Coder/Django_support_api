"""This is module for configuration API in Tickets component."""

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet

from tickets.models import Message, Ticket
from tickets.permissions import (
    IsManager,
    IsOwner,
    RoleIsAdmin,
    RoleIsManager,
    RoleIsUser,
)
from tickets.serializers import (
    MessageSerializer,
    TicketAssignSerializer,
    TicketSerializer,
)
from users.constants import Role

User = get_user_model()


class TicketAPIViewSet(ModelViewSet):
    """Class that defines user permissions."""

    serializer_class = TicketSerializer

    def get_queryset(self):
        """
        The function returns tickets from the database,
        taking into account rights.
        """
        user = self.request.user
        all_tickets = Ticket.objects.all()  # pylint: disable=E1101

        if user.role == Role.ADMIN:  # type: ignore
            return all_tickets
        if user.role == Role.MANAGER:  # type: ignore
            return all_tickets.filter(Q(manager=user) | Q(manager=None))
        # User`s rate fallback solution
        return all_tickets.filter(user=user)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions
        that this view requires.
        """
        match self.action:
            case "list":
                permission_classes = [RoleIsAdmin | RoleIsManager | RoleIsUser]
            case "create":
                permission_classes = [RoleIsUser]
            case "retrieve":
                permission_classes = [IsOwner | RoleIsAdmin | RoleIsManager]
            case "update":
                permission_classes = [RoleIsAdmin | RoleIsManager]
            case "destroy":
                permission_classes = [RoleIsAdmin | RoleIsManager]
            case "take":
                permission_classes = [RoleIsManager]
            case "reassign":
                permission_classes = [RoleIsAdmin & IsManager]
            case _:
                permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["put"])
    def take(self, request, pk):
        """A function that allows managers to take tickets for them selves."""

        ticket = self.get_object()

        if ticket.manager is not None:
            raise PermissionDenied(
                "A mamager is already assigned to this ticket"
            )

        serializer = TicketAssignSerializer(
            data={"manager_id": request.user.id}
        )
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)

    @action(detail=True, methods=["put"])
    def reassign(self, request, pk):
        """
        A function that allows the admin to reassign the ticket executor.
        """

        ticket = self.get_object()

        new_manager_id = request.data.get("new_manager")

        if ticket.manager_id == new_manager_id:
            raise ValidationError(
                "You cannot reassign a ticket to the same manager"
            )

        serializer = TicketAssignSerializer(
            data={"manager_id": new_manager_id}
        )
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)


class MessageListCreateAPIView(ListCreateAPIView):
    """Class that create users messages."""

    serializer_class = MessageSerializer
    lookup_field = "ticket_id"

    def get_queryset(self):
        return Message.objects.filter(  # pylint: disable=E1101
            Q(ticket__user=self.request.user)
            | Q(ticket__manager=self.request.user),
            ticket_id=self.kwargs[self.lookup_field],
        )

    @staticmethod
    def get_ticket(user: User, ticket_id: int) -> Ticket:  # type: ignore
        """Get ticket for current user."""

        tickets = Ticket.objects.filter(  # pylint: disable=E1101
            Q(user=user) | Q(manager=user)
        )

        return get_object_or_404(tickets, id=ticket_id)

    def post(self, request, ticket_id):
        ticket = self.get_ticket(request.user, ticket_id)
        payload = {
            "text": request.data["text"],
            "ticket": ticket.id,  # type: ignore
        }

        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
