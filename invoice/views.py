# invoice/views.py
import base64
import os
from django.contrib.staticfiles import finders
from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from django.conf import settings
from .models import Invoice


class InvoicePDFView(WeasyTemplateResponseMixin, DetailView):
    model = Invoice
    template_name = "invoice/invoice_template.html"
    pdf_attachment = False  # نمایش در مرورگر

    def _static_file_data_uri(self, static_path: str) -> str:
        """
        پیدا کردن فایل استاتیک و تبدیل به base64 (با پشتیبانی از PNG/JPG/TTF)
        """
        found = finders.find(static_path)
        if not found:
            return ""
        ext = os.path.splitext(found)[1].lower()
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".ttf": "font/ttf",
        }.get(ext, "application/octet-stream")

        with open(found, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{b64}"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # تصاویر
        ctx["logo_data"] = self._static_file_data_uri("invoice/logo.jpg")
        ctx["phone_icon"] = self._static_file_data_uri("invoice/icons8-phone-50.png")
        ctx["msg_icon"] = self._static_file_data_uri("invoice/icons8-message-50.png")
        ctx["telegram_icon"] = self._static_file_data_uri("invoice/icons8-telegram-24.png")

        # فونت فارسی
        ctx["font_data"] = self._static_file_data_uri("invoice/fonts/Vazir-Regular.ttf")

        # داده‌ها
        ctx["services"] = self.object.services.all()
        ctx["total"] = self.object.total_amount()

        return ctx

    def get_pdf_filename(self):
        return f"invoice-{self.object.invoice_number}.pdf"
