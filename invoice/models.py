from django.db import models
from django.db.models import Sum


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="شماره فاکتور") #اشکان فردا عدد میده از اون عدد به بعد شروع میشه
    date = models.DateField(verbose_name="تاریخ فاکتور") #تاریخ شمسی بشه
    business_name = models.CharField(max_length=200, verbose_name="نام صنف")
    agency_manager = models.CharField(max_length=100, verbose_name="مدیریت")
    license_number = models.CharField(max_length=100, default="14030455" , verbose_name="شماره مجوز")
    # address = pass
    # phone_number = pass
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتورها"

    def __str__(self):
        return f"فاکتور {self.invoice_number} - {self.business_name}"

    def total_amount(self):
        """جمع کل مبلغ خدمات فاکتور"""
        return self.services.aggregate(total=Sum("amount"))["total"] or 0


class ServiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="services")
    # service_name = models.CharField(max_length=200, verbose_name="نام خدمات")
    # منوی کشویی بزارم که بتونن پکیج پایه یا الماس بزارن
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="مبلغ (ریال)")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات") # این پارامتر باید چند تا اپشن بزاریم

    class Meta:
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"

    def __str__(self):
        return f"{self.service_name} - تعداد: {self.quantity}"
