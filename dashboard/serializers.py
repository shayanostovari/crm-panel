# dashboard/serializers.py
from rest_framework import serializers
from .models import Ticket, TicketMessage

class TicketMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = TicketMessage
        fields = ["id", "sender", "sender_name", "message", "created_at"]
        read_only_fields = ["id", "sender", "created_at"]


class TicketSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.username", read_only=True)
    team_name = serializers.CharField(source="assigned_team.name", read_only=True)
    messages = TicketMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id", "title", "description", "status",
            "created_by", "created_by_name",
            "assigned_team", "team_name",
            "created_at", "updated_at", "messages",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
