"""This is Admin module."""
from django.contrib import admin
from django.contrib.auth import get_user_model

from tickets.models import Message, Ticket

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Class to create Users Admin"""

    exclude = ["groups", "user_permissions", "password"]
    readonly_fields = [
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
        "email",
    ]
    list_filter = ["is_active", "role"]
    list_display = ["email", "first_name", "last_name", "role", "is_active"]
    search_fields = ["email", "last_name"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Class to create Tickets Admin Inerface"""

    list_display = ["title", "user", "manager", "status", "visibility"]
    search_fields = ["user", "manager", "status"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Class to create Messages Admin Inerface"""

    list_display = ["user", "ticket", "timestamp"]
    search_fields = ["user", "ticket", "timestamp"]
