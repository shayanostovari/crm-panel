# invoice/views.py
import base64
import os
from django.contrib.staticfiles import finders
from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from .models import Invoice


class InvoicePDFView(WeasyTemplateResponseMixin, DetailView):
    model = Invoice
    template_name = "invoice/invoice.html"   # قالب خودت
    pdf_attachment = False  # False = نمایش در مرورگر به جای دانلود

    def _img_data_uri(self, static_path: str) -> str:
        """ پیدا کردن فایل استاتیک و تبدیل به base64 """
        found = finders.find(static_path)
        if not found:
            return ""
        ext = os.path.splitext(found)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        with open(found, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{b64}"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # آیکون‌ها (که توی static/invoice/ داری)
        ctx["logo_data"] = self._img_data_uri("invoice/logo.png")            # مثلا اسمش logo.png
        ctx["phone_icon"] = self._img_data_uri("invoice/icons8-phone-50.png")
        ctx["msg_icon"] = self._img_data_uri("invoice/icons8-message-50.png")
        ctx["telegram_icon"] = self._img_data_uri("invoice/icons8-telegram-24.png")

        # اضافه: سرویس‌ها و جمع کل
        ctx["services"] = self.object.services.all()
        ctx["total"] = self.object.total_amount()

        return ctx

    def get_pdf_filename(self):
        return f"invoice-{self.object.invoice_number}.pdf"
