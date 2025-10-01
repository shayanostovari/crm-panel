from django.contrib import admin
from .models import Invoice, ServiceItem

class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("business_name", "invoice_number", "date", "agency_manager", "license_number", "created_at")
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
    )
