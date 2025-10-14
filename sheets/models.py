from django.db import models

class HamtiRecord(models.Model):
    تاریخ = models.CharField(max_length=50, blank=True, null=True)
    شهر = models.CharField(max_length=100, blank=True, null=True)
    منطقه = models.CharField(max_length=100, blank=True, null=True)
    کد_سفارش = models.CharField(max_length=50, unique=True, null=True, blank=True)
    نوع_کسب_کار = models.CharField(max_length=100, blank=True, null=True)
    حوزه_تخصصی = models.CharField(max_length=100, blank=True, null=True)
    نام_واحد_تجاری = models.CharField(max_length=255, blank=True, null=True)
    آدرس = models.TextField(blank=True, null=True)
    شماره_مشتری = models.CharField(max_length=355, blank=True, null=True)
    نام_مدیریت = models.CharField(max_length=200, blank=True, null=True)
    کارشناس_پیگیری = models.CharField(max_length=100, blank=True, null=True)
    مبلغ_توافق_شده = models.CharField(max_length=100, blank=True, null=True)
    مبلغ_فاکتور_شده = models.CharField(max_length=100, blank=True, null=True)
    مبلغ_واریز_شده = models.CharField(max_length=100, blank=True, null=True)
    قسط_اول = models.CharField(max_length=100, blank=True, null=True)
    قسط_دوم = models.CharField(max_length=100, blank=True, null=True)
    نتیجه_تماس = models.CharField(max_length=255, blank=True, null=True)
    وضعیت_درخواست_مشتری = models.CharField(max_length=255, blank=True, null=True)
    پیام_رسان_نمونه_کار = models.CharField(max_length=255, blank=True, null=True)
    وضعیت_ارسال = models.CharField(max_length=255, blank=True, null=True)
    مبدا_شماره = models.CharField(max_length=400, null=True, blank=True)
    مقصد = models.CharField(max_length=300, null=True, blank=True)
    ساعت_تماس_بعدی = models.CharField(max_length=50, null=True, blank=True)
    پیغام_مدیر = models.CharField(max_length=500, null=True, blank=True)
    زمان_تمدید = models.CharField(max_length=50, null=True, blank=True)
    توضیحات_نمونه_کار = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.کد_سفارش} - {self.نام_واحد_تجاری or 'بی‌نام'}"
