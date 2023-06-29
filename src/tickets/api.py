"""This is module for configuration API in Tickets component."""

from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tickets.models import Ticket
from tickets.permissions import IsOwner, RoleIsAdmin, RoleIsManager, RoleIsUser
from tickets.serializers import TicketAssignSerializer, TicketSerializer
from users.constants import Role


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
                permission_classes = [RoleIsAdmin]
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

        manager_id = request.data.get("manager_id")

        serializer = TicketAssignSerializer(data={"manager_id": manager_id})
        serializer.is_valid()
        ticket = serializer.assign(ticket)

        return Response(TicketSerializer(ticket).data)


class MessageListCreateAPIView(ListCreateAPIView):
    """Class that create users messages."""

    serializer_class = TicketSerializer

    def get_queryset(self):
        return
