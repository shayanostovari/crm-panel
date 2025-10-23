import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import arabic_reshaper
from bidi.algorithm import get_display
from textwrap import wrap
import jdatetime

from .models import Invoice, ServiceItem


def generate_invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    services = ServiceItem.objects.filter(invoice=invoice)

    response = HttpResponse(content_type="application/pdf")
    filename = f"فاکتور_{invoice.invoice_number}.pdf"
    response["Content-Disposition"] = f'inline; filename="{filename}"'

    jalali_date = jdatetime.date.fromgregorian(date=invoice.date)
    jalali_date_str = f"{jalali_date.year}/{jalali_date.month}/{jalali_date.day}"

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    margin = 40

    # paths to fonts
    font_path = os.path.join(
        settings.BASE_DIR, "invoice", "static", "invoice", "fonts", "BTitrBold_0.ttf"
    )
    nazanin_path = os.path.join(
        settings.BASE_DIR, "invoice", "static", "invoice", "fonts", "B-NAZANIN.TTF"
    )

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"فونت پیدا نشد: {font_path}")
    pdfmetrics.registerFont(TTFont("Titr", font_path))

    if not os.path.exists(nazanin_path):
        raise FileNotFoundError(f"فونت پیدا نشد: {nazanin_path}")
    pdfmetrics.registerFont(TTFont("Nazanin", nazanin_path))

    # helper for Farsi display
    def farsi(text):
        if not text:
            return ""
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)

    # helper for wrapping text
    def fit_text(text, max_chars_per_line=60):
        return wrap(str(text), max_chars_per_line)

    # background image
    bg_path = os.path.join(
        settings.BASE_DIR, "invoice", "static", "invoice", "pics", "invoice_template.png"
    )
    if os.path.exists(bg_path):
        c.drawImage(bg_path, 0, 0, width=width, height=height, preserveAspectRatio=True)

    # font sizes
    default_font_size = 11  # ثابت برای متن‌های عمومی
    special_font_size = invoice.font_size or default_font_size

    # invoice header (سایز ثابت)
    c.setFont("Titr", default_font_size)
    c.drawString(90, height - margin - 76, farsi(f"شماره فاکتور: {invoice.invoice_number}"))
    c.drawString(88, height - margin - 98, farsi(f"تاریخ: {jalali_date_str}"))

    y = height - margin - 120
    c.drawRightString(width - margin - 8, y + 1, farsi(f"شماره مجوز: {invoice.license_number or '-'}"))
    c.drawRightString(width - margin - 11, y - 56, farsi(f"مدیریت: {invoice.agency_manager or '-'}"))
    c.drawRightString(width - margin - 360, y - 56, farsi(f"نام صنف: {invoice.business_name or '-'}"))

    # address (فقط از فیلد address و با سایز خاص)
    c.setFont("Titr", special_font_size)
    address_lines = fit_text(invoice.address or '-', 60)
    for i, line in enumerate(address_lines):
        c.drawRightString(
            width - margin - 10,
            y - 108 - (i * (special_font_size + 2)),
            farsi(line)
        )

    # phone numbers (سایز خاص)
    c.setFont("Titr", special_font_size)
    c.drawRightString(
        width - margin - 10,
        y - 127 - (len(address_lines) * (special_font_size + 2)),
        farsi(f"تماس: {invoice.phone_numbers or '-'}")
    )

    # service first description (سایز خاص)
    if services.exists():
        c.setFont("Titr", special_font_size)
        # شکستن متن بر اساس خط‌های جدید (Shift+Enter) یا طول زیاد
        raw_lines = (services[0].description or '-').splitlines()
        desc_texts = []
        for line in raw_lines:
            desc_texts.extend(fit_text(line, 60))  # حتی اگه یک خط طولانی بود، بشکنش

        base_y = y - 210
        for i, line in enumerate(desc_texts):
            c.drawRightString(
                width - margin - 263,
                base_y - (i * (special_font_size + 3)),  # فاصله بیشتر بین خطوط
                farsi(line)
            )

    # invoice general description (سایز ثابت)
    c.setFont("Titr", default_font_size)
    c.drawRightString(width - margin - 263, y - 300, farsi(f"{invoice.description or '-'}"))

    # services table
    total = 0
    len_s = 0
    for s in services:
        y_s = 195
        total += s.amount or 0
        len_s += 20
        amount_str = f"{int(s.amount):,}" if s.amount else "0"

        # service name (سایز ثابت بزرگ‌تر)
        c.setFont("Nazanin", default_font_size + 3)
        c.drawRightString(
            width - margin - 40,
            y - (y_s + len_s),
            farsi(f"{s.name_farsi}")
        )

        # quantity and amount (سایز ثابت)
        c.setFont("Titr", default_font_size)
        c.drawRightString(width - margin - 142, y - (y_s + len_s), farsi(f"{s.quantity}"))
        c.drawRightString(width - margin - 190, y - (y_s + len_s), farsi(f"{amount_str * s.quantity}"))

    # total amount (سایز ثابت)
    total_str = f"{int(total):,}"
    c.drawRightString(width - margin - 190, y - 345, farsi(f"{total_str}"))

    c.showPage()
    c.save()

    return response
