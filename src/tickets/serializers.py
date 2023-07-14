"""This is module for configuration serializers in Ticket component."""

from rest_framework import serializers

from tickets.models import Message, Ticket


class TicketSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "text",
            "visibility",
            "status",
            "user",
            "manager",
        ]
        read_only_fields = ["visibility", "manager"]


class TicketAssignSerializer(serializers.Serializer):
    manager_id = serializers.IntegerField()

    def assign(self, ticket: Ticket) -> Ticket:
        ticket.manager_id = self.validated_data["manager_id"]  # type: ignore
        ticket.save()

        return ticket


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ["id", "text", "user", "ticket", "timestamp"]
        read_only_fields = ["id", "timestamp"]
