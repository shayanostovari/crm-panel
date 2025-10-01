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
