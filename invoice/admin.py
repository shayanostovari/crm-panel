# invoice/admin.py
from django.contrib import admin
from .models import Invoice, ServiceItem

class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1
    fields = ("service_name", "quantity", "amount", "description", "line_total")
    readonly_fields = ("line_total",)

    def line_total(self, obj):
        return obj.total
    line_total.short_description = "جمع سطر"

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("business_name", "invoice_number", "get_jalali_date", "agency_manager", "license_number", "total_amount_display", "created_at")
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
        return format(obj.total_amount(), ",")
    total_amount_display.short_description = "جمع کل (ریال)"

    def get_jalali_date(self, obj):
        return obj.get_jalali_date()
    get_jalali_date.short_description = "تاریخ (شمسی)"
