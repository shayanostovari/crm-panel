from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Invoice, ServiceItem


class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1
    fields = ('service_name', 'quantity', 'amount', 'description')
    verbose_name = "خدمت"
    verbose_name_plural = "خدمات"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'invoice_number',
        'business_name',
        'agency_manager',
        'total_price_display',
        'invoice_date_jalali',
        'pdf_link',
    )
    list_display_links = ('id', 'business_name')
    search_fields = ('invoice_number', 'business_name', 'agency_manager', 'license_number')
    ordering = ('-id',)
    inlines = [ServiceItemInline]

    def total_price_display(self, obj):
        try:
            total = obj.total_amount()
            return f"{total:,.0f} ریال"
        except Exception:
            return "—"
    total_price_display.short_description = "جمع کل"

    def invoice_date_jalali(self, obj):
        return obj.get_jalali_date()
    invoice_date_jalali.short_description = "تاریخ فاکتور"

    def pdf_link(self, obj):
        url = reverse('invoice-pdf', args=[obj.pk])
        return format_html('<a href="{}" target="_blank">📄 نمایش PDF</a>', url)
    pdf_link.short_description = "PDF فاکتور"
