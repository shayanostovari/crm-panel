from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from .models import Invoice, ServiceItem


class InvoiceAdminForm(forms.ModelForm):
    """فرم سفارشی برای کنترل ساعت ارسال (HH:MM)"""
    class Meta:
        model = Invoice
        fields = "__all__"
        widgets = {
            "send_time": forms.TimeInput(format="%H:%M"),
        }


class ServiceItemInline(admin.TabularInline):
    """نمایش خدمات مربوطه در پایین صفحه فاکتور داخل پنل ادمین"""
    model = ServiceItem
    extra = 1
    fields = ("service_name", "quantity", "amount", "description")
    verbose_name = "خدمت"
    verbose_name_plural = "خدمات"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """مدیریت فاکتورها در پنل ادمین"""
    form = InvoiceAdminForm
    list_display = (
        "id",
        "invoice_number",
        "business_name",
        "agency_manager",
        "total_price_display",
        "invoice_date_jalali",
        "send_time",
        "pdf_link",
    )
    list_display_links = ("id", "business_name")
    search_fields = ("invoice_number", "business_name", "agency_manager", "license_number")
    ordering = ("-id",)
    inlines = [ServiceItemInline]

    def total_price_display(self, obj):
        """نمایش جمع کل فاکتور با فرمت هزارگان"""
        try:
            total = obj.total_amount()
            return f"{total:,.0f} ریال"
        except Exception:
            return "—"

    total_price_display.short_description = "جمع کل"

    def invoice_date_jalali(self, obj):
        """نمایش تاریخ شمسی"""
        return obj.get_jalali_date()

    invoice_date_jalali.short_description = "تاریخ فاکتور"

    def pdf_link(self, obj):
        """نمایش لینک مستقیم به PDF فاکتور"""
        url = reverse("invoice-pdf", args=[obj.pk])
        return format_html('<a href="{}" target="_blank">📄 نمایش PDF</a>', url)

    pdf_link.short_description = "PDF فاکتور"
