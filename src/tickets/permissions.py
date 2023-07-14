"""This is module for configuration permissions in Ticket component."""

from rest_framework.permissions import BasePermission

from tickets.models import Ticket
from users.constants import Role
from users.models import User


class RoleIsAdmin(BasePermission):
    """Class that grants Admin rights."""

    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN  # type: ignore


class RoleIsManager(BasePermission):
    """Class that grants Manager rights."""

    def has_permission(self, request, view):
        return request.user.role == Role.MANAGER  # type: ignore


class IsManager(BasePermission):
    """
    Class that grants, only allow managers to be assigned to tickets.
    """

    def has_permission(self, request, view):
        new_manager_id = request.data.get("new_manager")
        manager = User.objects.get(id=new_manager_id)
        return manager.role == Role.MANAGER  # type: ignore


class RoleIsUser(BasePermission):
    """Class that grants User rights."""

    def has_permission(self, request, view):
        return request.user.role == Role.USER  # type: ignore


class IsOwner(BasePermission):
    """Class that grants Tickets Owner rights."""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj: Ticket):
        return obj.user == request.user
