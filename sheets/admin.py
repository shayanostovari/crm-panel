from django.contrib import admin
from .models import HamtiRecord

@admin.register(HamtiRecord)
class HamtiRecordAdmin(admin.ModelAdmin):
    list_display = (
        "کد_سفارش",
        "نام_واحد_تجاری",
        "شهر",
        "کارشناس_پیگیری",
        "مبلغ_توافق_شده",
        "وضعیت_درخواست_مشتری",
    )
    search_fields = ("کد_سفارش", "نام_واحد_تجاری", "کارشناس_پیگیری", "شهر")
    list_filter = ("شهر", "کارشناس_پیگیری", "وضعیت_درخواست_مشتری")
