from django.contrib import admin
from .models import Team, Ticket, TicketMessage
from django.contrib.auth import get_user_model

User = get_user_model()


# -------------------------------
# 👥 Team Admin
# -------------------------------
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("members",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.teams.filter(name="manager").exists():
            return qs
        return qs.filter(members=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.teams.filter(name="manager").exists():
            return True
        if request.user.teams.filter(name="sales").exists():
            return False
        if request.user.teams.filter(name="tech").exists():
            return True if obj is None else False
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.teams.filter(name="manager").exists():
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.teams.filter(name__in=["manager", "tech"]).exists():
            return True
        return False


# -------------------------------
# 💬 TicketMessage Inline
# -------------------------------
class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 1
    readonly_fields = ("sender", "created_at")
    fields = ("sender", "message", "created_at")
    can_delete = True


# -------------------------------
# 🎫 Ticket Admin
# -------------------------------
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_team", "status", "created_by", "created_at")
    list_filter = ("status", "assigned_team")
    search_fields = ("title", "description", "created_by__username")
    readonly_fields = ("created_by", "created_at", "updated_at")
    inlines = [TicketMessageInline]

    def save_model(self, request, obj, form, change):
        """در زمان ایجاد تیکت، کاربر فعلی را به عنوان ایجادکننده ذخیره کن"""
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """ست کردن sender برای inline messages"""
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.sender_id:
                instance.sender = request.user
            instance.save()
        formset.save_m2m()


# -------------------------------
# 🗨️ TicketMessage Admin
# -------------------------------
@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ("ticket", "sender", "created_at")
    search_fields = ("message", "sender__username", "ticket__title")
    readonly_fields = ("created_at",)
