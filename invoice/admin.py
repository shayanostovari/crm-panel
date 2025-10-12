from django.contrib import admin
from .models import Invoice
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    # ستون‌هایی که در لیست فاکتورها در پنل مدیریتی نمایش داده می‌شوند
    list_display = (
        'id',
        'business_name',          # فیلد موجود در مدل Invoice
        'agency_manager',         # مدیر مسئول
        'total_price_display',    # نمایش مبلغ کل به صورت فرمت‌شده
        'invoice_date_jalali',    # تاریخ شمسی
        'pdf_link',               # لینک دانلود PDF
    )
    list_display_links = ('id', 'business_name')
    search_fields = ('business_name', 'agency_manager', 'license_number', 'id')
    ordering = ('-id',)

    def total_price_display(self, obj):
        """نمایش مبلغ کل فاکتور به صورت فارسی و با جداکننده هزارگان"""
        try:
            total = obj.total_amount()  # فراخوانی تابع محاسبه مجموع در مدل
            return f"{total:,.0f} تومان"
        except Exception:
            return "-"
    total_price_display.short_description = "مبلغ کل"

    def invoice_date_jalali(self, obj):
        """تبدیل تاریخ فاکتور به فرمت شمسی خوانا"""
        return obj.get_jalali_date()
    invoice_date_jalali.short_description = "تاریخ فاکتور"

    def pdf_link(self, obj):
        """ایجاد لینک قابل کلیک برای دانلود فایل PDF فاکتور"""
        url = reverse('invoice-pdf', args=[obj.pk])
        return format_html('<a href="{}" target="_blank">📄 دانلود PDF</a>', url)
    pdf_link.short_description = "دانلود PDF"
