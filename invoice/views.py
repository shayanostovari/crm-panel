# invoice/views.py
import base64
import os
from django.contrib.staticfiles import finders
from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from .models import Invoice


class InvoicePDFView(WeasyTemplateResponseMixin, DetailView):
    model = Invoice
    template_name = "invoice/invoice_template.html"
    pdf_attachment = False  # False => نمایش در مرورگر، True => دانلود

    # ======== Helper Functions ========

    def _file_to_data_uri(self, static_path: str, mime: str) -> str:
        """خواندن فایل از استاتیک و تبدیل به data URI"""
        found = finders.find(static_path)
        if not found:
            return ""
        with open(found, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{b64}"

    def _img_data_uri(self, static_path: str) -> str:
        """تبدیل عکس به data URI"""
        found = finders.find(static_path)
        if not found:
            return ""
        ext = os.path.splitext(found)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        return self._file_to_data_uri(static_path, mime)

    def _font_data_uri(self, static_path: str) -> str:
        """تبدیل فونت ttf به data URI"""
        return self._file_to_data_uri(static_path, "font/ttf")

    def _inline_css(self, static_css_path: str, font_map: dict) -> str:
        """
        خواندن فایل CSS و جایگزین کردن لینک فونت‌های نسبی با data-uri های موجود در font_map
        بعلاوه اضافه کردن helper CSS مخصوص WeasyPrint
        """
        found = finders.find(static_css_path)
        if not found:
            return ""
        with open(found, "r", encoding="utf-8") as f:
            css = f.read()

        # جایگزینی مسیر فونت‌ها با data-uri
        for rel_path, data_uri in font_map.items():
            css = css.replace(f"url('{rel_path}')", f"url('{data_uri}')")
            css = css.replace(f'url("{rel_path}")', f'url("{data_uri}")')
            css = css.replace(f"url({rel_path})", f"url({data_uri})")
            css = css.replace(rel_path, data_uri)

        css += """
html, body { direction: rtl; unicode-bidi: embed; }
table { table-layout: fixed; width: 100%; border-collapse: collapse; }
th, td { word-wrap: break-word; vertical-align: top; }
"""
        return css

    # ======== Context ========

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # تصاویر
        ctx["logo_data"] = self._img_data_uri("invoice/pics/logo.jpg")
        ctx["phone_icon"] = self._img_data_uri("invoice/pics/icons8-phone-50.png")
        ctx["msg_icon"] = self._img_data_uri("invoice/pics/icons8-message-50.png")
        ctx["telegram_icon"] = self._img_data_uri("invoice/pics/icons8-telegram-24.png")

        # فونت‌ها (Vazirmatn)
        font_reg = self._font_data_uri("invoice/fonts/Vazirmatn-Regular.ttf")
        font_bold = self._font_data_uri("invoice/fonts/Vazirmatn-Bold.ttf")
        ctx["font_data"] = font_reg
        ctx["font_data_bold"] = font_bold

        # inline CSS
        font_map = {
            "../fonts/Vazirmatn-Regular.ttf": font_reg,
            "../fonts/Vazirmatn-Bold.ttf": font_bold,
            "invoice/fonts/Vazirmatn-Regular.ttf": font_reg,
            "invoice/fonts/Vazirmatn-Bold.ttf": font_bold,
        }
        ctx["inline_css"] = self._inline_css("invoice/css/invoice_style.css", font_map)

        # داده‌های فاکتور
        services_qs = self.object.services.all().order_by("id")
        services = list(services_qs)
        ctx["services"] = services
        ctx["total"] = self.object.total_amount()

        # بررسی اینکه آیا هیچ خدمتی توضیح دارد یا نه
        ctx["has_service_descriptions"] = any(bool(s.description) for s in services)

        return ctx

    # ======== Filename ========

    def get_pdf_filename(self):
        return f"invoice-{self.object.invoice_number}.pdf"
