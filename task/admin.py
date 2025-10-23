from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description", "creator__username")
    filter_horizontal = ("assignees",)
    readonly_fields = ("created_at", "updated_at")
