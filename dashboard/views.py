

# dashboard/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ticket, TicketMessage, Team
from .serializers import TicketSerializer, TicketMessageSerializer
from django.shortcuts import get_object_or_404

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related("created_by", "assigned_team")
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # مدیر می‌بیند همه تیکت‌ها
        if user.is_superuser or user.teams.filter(name="manager").exists():
            return Ticket.objects.all()
        # سایر اعضا فقط تیکت‌های مربوط به تیم خودشون
        return Ticket.objects.filter(assigned_team__in=user.teams.all())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["get", "post"])
    def messages(self, request, pk=None):
        """نمایش یا افزودن پیام به تیکت"""
        ticket = get_object_or_404(Ticket, pk=pk)
        if request.method == "GET":
            messages = ticket.messages.select_related("sender").all()
            return Response(TicketMessageSerializer(messages, many=True).data)
        elif request.method == "POST":
            serializer = TicketMessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(ticket=ticket, sender=request.user)
            return Response(serializer.data, status=201)
