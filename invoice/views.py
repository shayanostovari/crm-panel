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
from reportlab.lib.colors import red, black   # ✅ رنگ‌ها اضافه شدند

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

    # فاکتور عضویت
    c.setFont("Titr", 17)
    title_text = farsi("فاکتور عضویت اصناف شهر")
    c.drawString(220, height - 151, title_text)

    # کانون آگهی و تبلیغات بازارسازان هوشمند پویا
    c.setFont("Titr", 11)
    title_text = farsi("کانون آگهی و تبلیغات بازارسازان هوشمند پویا")
    c.drawString(380, height - 76, title_text)

    # دارای مجوز رسمی از وزارت فرهنگ و ارشاد اسلامی
    c.setFont("Titr", 11)
    title_text = farsi("دارای مجوز رسمی از وزارت فرهنگ و ارشاد اسلامی")
    c.drawString(355, height - 100, title_text)

    # نام خدمات
    c.setFont("Titr", 12)
    c.drawString(473, height - 340, farsi("نام خدمات"))

    # تعداد
    c.setFont("Titr", 12)
    c.drawString(400, height - 340, farsi("تعداد"))

    # مبلغ کل
    c.setFont("Titr", 12)
    c.drawString(310, height - 340, farsi("مبلغ کل (ریال)"))

    # خدمات در وبسایت اصناف شهر
    c.setFont("Titr", 12)
    c.drawString(120, height - 340, farsi("خدمات در وبسایت اصناف شهر"))

    # توضیحات
    c.setFont("Titr", 10)
    c.drawString(260, height - 477, farsi("توضیحات"))

    # جمع فاکتور
    c.setFont("Titr", 11)
    c.drawString(475, height - 537, farsi("جمع فاکتور"))

    # کد مشاور
    c.setFont("Titr", 11)
    c.drawString(395, height - 537, farsi("کد مشاور"))

    # ساعت ارسال
    c.setFont("Titr", 11)
    c.drawString(160, height - 537, farsi("ساعت ارسال"))

    # شرح خدمات
    c.setFont("Titr", 11)
    c.drawString(467, height - 570, farsi("شرح خدمات:"))

    # با دریافت خدمات میتوانید
    c.setFont("Nazanin", 11)
    c.drawString(200, height - 595, farsi(" با دریافت خدمات میتوانید از 10 صبح الی 18 بعد از ظهر با مشاوران بازرگانی ما در زمینه بهبود"))

    # فروش و بازاریابی برای کسب و کارتان مشورت بگیرید
    c.setFont("Nazanin", 11)
    c.drawString(335, height - 605, farsi("فروش و بازاریابی برای کسب و کارتان مشورت بگیرید"))

    # تمامی موارد ذکر شده، ...
    c.setFont("Nazanin", 11)
    c.drawString(190, height - 625, farsi("تمامی موارد ذکر شده، پس از واریز وجه ،در مدت 20 روز کاری،نشر و به شما نمایش داده خواهد شد"))

    # 🔴 تماس با پشتیبانی (واتساپ)
    c.setFont("Titr", 12)
    c.setFillColor(red)   # رنگ قرمز فقط برای این متن
    s = "تماس با پشتیبانی (واتساپ) : 3823039-0992"
    c.drawString(290, height - 662, farsi(s))
    c.setFillColor(black)   # ✅ بازگرداندن رنگ مشکی برای بخش‌های بعدی

    #شماره کارت : 9285-4950-7210-5041
    c.setFont("Nazanin", 11)
    c.drawString(350, height - 695, farsi(" شماره کارت : 9285-4950-7210-5041"))

    #آقای علیرضا حسینعلی - بانک رسالت
    c.setFont("Nazanin", 11)
    c.drawString(150, height - 695, farsi("آقای علیرضا حسینعلی - بانک رسالت"))

    #شماره شبا:97070000001000115568446001
    c.setFont("Nazanin", 11)
    c.drawString(330, height - 710, farsi("شماره شبا: 97070000001000115568446001"))


    #آقای علیرضا حسینعلی - بانک رسالت
    c.setFont("Nazanin", 11)
    c.drawString(150, height - 710, farsi("آقای علیرضا حسینعلی - بانک رسالت"))

    #امضای تحویل گیرنده
    c.setFont("Nazanin", 11)
    c.drawString(92, height - 755, farsi("امضای تحویل گیرنده:"))

    #44782151-44780156
    c.setFont("Titr", 11)
    c.drawString(420, height - 780, farsi("44782151-44780156"))

    #www.asnafeshahr.com
    c.setFont("Helvetica", 11)  # 🔹 فونت لاتین استاندارد در ReportLab
    c.drawString(412, height - 805, "www.asnafeshahr.com")

    #تهران، کیلومتر14 جاده مخصوص،خیابان 55
    c.setFont("Titr", 11)
    c.drawString(190, height - 827, farsi("تهران، کیلومتر14 جاده مخصوص،خیابان 55 شهرک غزالی،خیابان توران بهشتی، پلاک 1"))



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
                farsi(wline),
            )

    # شماره تماس
    c.drawRightString(
        width - margin - 10,
        y - 85 - (len(raw_lines) * (special_font_size + 2)),
        farsi(f"تماس: {invoice.phone_numbers or '-'}"),
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
                farsi(line),
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
