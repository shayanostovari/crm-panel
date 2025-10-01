# dashboard/admin.py
from django.contrib import admin
from .models import Team
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("members",)

    # محدود کردن queryset بر اساس تیم
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # مدیر تیم می‌بیند همه تیم‌ها
        if request.user.teams.filter(name="manager").exists():
            return qs
        # برای دیگر تیم‌ها فقط تیم خودشون
        return qs.filter(members=request.user)

    # دسترسی به تغییر و حذف
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.teams.filter(name="manager").exists():
            return True  # Manager full access
        if request.user.teams.filter(name="sales").exists():
            return False  # Sales can only READ
        if request.user.teams.filter(name="tech").exists():
            return True if obj is None else False  # Tech can CREATE (obj is None) but not CHANGE
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.teams.filter(name="manager").exists():
            return True
        return False  # فقط Manager می‌تواند حذف کند

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.teams.filter(name__in=["manager", "tech"]).exists():
            return True  # Manager و Tech می‌توانند اضافه کنند
        return False
