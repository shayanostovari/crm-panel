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

    # تبدیل تاریخ میلادی به شمسی
    jalali_date = jdatetime.date.fromgregorian(date=invoice.date)
    jalali_date_str = f"{jalali_date.year}/{jalali_date.month}/{jalali_date.day}"

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    margin = 40

    # مسیر فونت‌ها
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

    # کمک‌کننده برای نمایش فارسی
    def farsi(text):
        if not text:
            return ""
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)

    # کمک‌کننده برای شکستن متن طولانی
    def fit_text(text, max_chars_per_line=60):
        return wrap(str(text), max_chars_per_line)

    # پس‌زمینه فاکتور
    bg_path = os.path.join(
        settings.BASE_DIR, "invoice", "static", "invoice", "pics", "invoice_template.png"
    )
    if os.path.exists(bg_path):
        c.drawImage(bg_path, 0, 0, width=width, height=height, preserveAspectRatio=True)

    # سایز فونت‌ها
    default_font_size = 11
    special_font_size = invoice.font_size or default_font_size

    # --- سربرگ فاکتور ---
    c.setFont("Titr", default_font_size)
    c.drawString(90, height - margin - 30, farsi(f"شماره فاکتور: {invoice.invoice_number}"))
    c.drawString(88, height - margin - 45, farsi(f"تاریخ: {jalali_date_str}"))

    # 👇 ساعت ارسال (از پنل ادمین)
    if invoice.send_time:
        formatted_send_time = invoice.send_time.strftime("%H:%M")
    else:
        formatted_send_time = "—"
    # پایین صفحه سمت چپ
    c.setFont("Nazanin", 10)
    c.drawString(130, 305, farsi(formatted_send_time))

    y = height - margin - 120
    c.setFont("Titr", default_font_size)
    c.drawRightString(width - margin - 8, y + 40, farsi(f"شماره مجوز: {invoice.license_number or '-'}"))
    c.drawRightString(width - margin - 11, y - 20, farsi(f"مدیریت: {invoice.agency_manager or '-'}"))
    c.drawRightString(width - margin - 330, y - 20, farsi(f"نام صنف: {invoice.business_name or '-'}"))

    # آدرس (شماره‌دار)
    c.setFont("Nazanin", special_font_size)
    raw_lines = (invoice.address or '-').splitlines()

    for i, line in enumerate(raw_lines):
        numbered_line = f"{i + 1} - {line.strip()}"
        wrapped_lines = fit_text(numbered_line, 60)
        for j, wline in enumerate(wrapped_lines):
            c.drawRightString(
                width - margin - 10,
                y - 45 - ((i + j) * (special_font_size + 3)),
                farsi(wline)
            )

    # شماره تماس — ✅ اصلاح شد: استفاده از raw_lines
    c.drawRightString(
        width - margin - 10,
        y - 85 - (len(raw_lines) * (special_font_size + 2)),
        farsi(f"تماس: {invoice.phone_numbers or '-'}")
    )

    # توضیح اولین خدمت
    if services.exists():
        c.setFont("Nazanin", special_font_size)
        service_lines = (services[0].description or '-').splitlines()
        desc_texts = []
        for line in service_lines:
            desc_texts.extend(fit_text(line, 60))

        base_y = y - 210
        for i, line in enumerate(desc_texts):
            c.drawRightString(
                width - margin - 263,
                base_y - (i * (special_font_size + 3)),
                farsi(line)
            )

    # توضیحات عمومی فاکتور
    c.setFont("Nazanin", default_font_size)
    c.drawRightString(width - margin - 263, y - 335, farsi(f"{invoice.description or '-'}"))

    # جدول خدمات
    total = 0
    len_s = 0
    for s in services:
        y_s = 195
        total += s.amount or 0
        len_s += 20
        amount_str = f"{int(s.amount):,}" if s.amount else "0"

        c.setFont("Nazanin", default_font_size + 3)
        c.drawRightString(width - margin - 40, y - (y_s + len_s), farsi(f"{s.name_farsi}"))

        c.setFont("Nazanin", default_font_size)
        c.drawRightString(width - margin - 142, y - (y_s + len_s), farsi(str(s.quantity)))
        c.drawRightString(width - margin - 190, y - (y_s + len_s), farsi(f"{amount_str * s.quantity}"))

    # جمع کل
    total_str = f"{int(total):,}"
    c.drawRightString(width - margin - 187, y - 376, farsi(total_str))

    c.showPage()
    c.save()
    return response
