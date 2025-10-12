from django.db import models
from django.conf import settings


class Team(models.Model):
    TEAM_CHOICES = [
        ("manager", "Manager"),
        ("sales", "Sales"),
        ("tech", "Tech"),
    ]

    name = models.CharField(max_length=50, choices=TEAM_CHOICES, unique=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        blank=True
    )

    def __str__(self):
        return self.get_name_display()


class Ticket(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("closed", "Closed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tickets"
    )
    assigned_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class TicketMessage(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} on {self.ticket}"
