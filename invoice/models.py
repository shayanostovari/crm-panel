from decimal import Decimal
import jdatetime
from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

SERVICE_CHOICES = [
    ("paye", "پکیج پایه"),
    ("almas", "پکیج الماس"),
]

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="شماره فاکتور")
    date = models.DateField(verbose_name="تاریخ فاکتور")
    business_name = models.CharField(max_length=200, verbose_name="نام صنف")
    agency_manager = models.CharField(max_length=100, verbose_name="مدیریت")
    license_number = models.CharField(max_length=100, default="14030455", verbose_name="شماره مجوز")
    address = models.CharField(max_length=200, verbose_name="آدرس")
    phone_number = models.CharField(max_length=20, verbose_name="شماره تلفن")
    description = models.TextField(verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتورها"

    def __str__(self):
        return f"فاکتور {self.invoice_number} - {self.business_name}"

    def total_amount(self):
        total = self.services.aggregate(
            total=Sum(
                ExpressionWrapper(F("amount") * F("quantity"), output_field=DecimalField())
            )
        )["total"] or Decimal(0)
        return total

    def get_jalali_date(self):
        if not self.date:
            return ""
        j = jdatetime.date.fromgregorian(date=self.date)
        return j.strftime("%Y/%m/%d")


class ServiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="services")
    service_name = models.CharField(max_length=50, choices=SERVICE_CHOICES, verbose_name="نام خدمات")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="مبلغ کل (ریال)")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "خدمات"
        verbose_name_plural = "خدمات"

    def __str__(self):
        return f"{self.get_service_name_display()} - تعداد: {self.quantity}"

    @property
    def total(self):
        return (self.amount or 0) * (self.quantity or 1)
