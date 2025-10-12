# invoice/admin.py
from django.contrib import admin
from .models import Invoice, ServiceItem


class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1
    fields = ("service_name", "quantity", "amount", "description", "line_total")
    readonly_fields = ("line_total",)

    def line_total(self, obj):
        try:
            return format(obj.total or 0, ",")
        except Exception:
            return "0"
    line_total.short_description = "جمع سطر"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "invoice_number",
        "get_jalali_date_safe",
        "agency_manager",
        "license_number",
        "total_amount_display",
        "created_at",
        "description",
    )
    search_fields = ("invoice_number", "business_name")
    list_filter = ("date", "created_at")
    ordering = ("-date",)
    inlines = [ServiceItemInline]

    fields = (
        "invoice_number",
        "date",
        "business_name",
        "agency_manager",
        "license_number",
        "address",
        "phone_number",
    )

    def total_amount_display(self, obj):
        """
        نمایش امن جمع کل فاکتور در ادمین — بدون خطا اگر هیچ خدمت نداشت.
        """
        try:
            total = obj.total_amount() or 0
            return format(total, ",")
        except Exception as e:
            return f"0 (⚠️ خطا در محاسبه)"
    total_amount_display.short_description = "جمع کل (ریال)"

    def get_jalali_date_safe(self, obj):
        """
        نمایش تاریخ شمسی به‌صورت امن (در صورت نبود تاریخ یا خطا)
        """
        try:
            return obj.get_jalali_date() or "-"
        except Exception:
            return "-"
    get_jalali_date_safe.short_description = "تاریخ (شمسی)"