from django.contrib import admin
from .models import Invoice
from django.utils.html import format_html
from django.urls import reverse

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'total_price_display',
        'invoice_date_jalali',
        'pdf_link',
    )
    list_display_links = ('id', 'customer_name')
    search_fields = ('customer_name', 'id')
    ordering = ('-id',)

    def total_price_display(self, obj):
        return f"{obj.total_price:,.0f} تومان"
    total_price_display.short_description = "مبلغ فاکتور"

    def invoice_date_jalali(self, obj):
        return obj.get_jalali_date()
    invoice_date_jalali.short_description = "تاریخ فاکتور"

    def pdf_link(self, obj):
        url = reverse('invoice-pdf', args=[obj.pk])
        return format_html('<a href="{}" target="_blank">📄 دانلود PDF</a>', url)
    pdf_link.short_description = "دانلود PDF"
