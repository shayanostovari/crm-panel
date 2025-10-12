import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML, CSS
from .models import Invoice, ServiceItem


def generate_invoice_pdf(request, pk):
    # پیدا کردن فاکتور مربوطه
    invoice = get_object_or_404(Invoice, pk=pk)
    services = ServiceItem.objects.filter(invoice=invoice)

    # مسیر فایل‌های استاتیک برای Liara (file://)
    logo_path = f"file://{os.path.join(settings.STATIC_ROOT, 'invoice/pics/logo.jpg')}"
    address_icon = f"file://{os.path.join(settings.STATIC_ROOT, 'invoice/pics/address.png')}"
    website_icon = f"file://{os.path.join(settings.STATIC_ROOT, 'invoice/pics/website.png')}"
    phone_icon = f"file://{os.path.join(settings.STATIC_ROOT, 'invoice/pics/phone.png')}"
    instagram_icon = f"file://{os.path.join(settings.STATIC_ROOT, 'invoice/pics/instagram.png')}"

    # قالب HTML
    template = get_template("invoice_template.html")

    # کانتکست داده‌ها
    context = {
        "object": invoice,
        "services": services,
        "logo_data": logo_path,
        "address_icon": address_icon,
        "website_icon": website_icon,
        "phone_icon": phone_icon,
        "instagram_icon": instagram_icon,
    }

    # رندر قالب HTML با داده‌ها
    html_string = template.render(context)

    # مسیر فونت و CSS
    css_path = os.path.join(settings.STATIC_ROOT, "invoice/css/invoice_pdf.css")
    pdf_font_path = os.path.join(settings.STATIC_ROOT, "invoice/fonts/Vazirmatn-Regular.ttf")

    # ساخت خروجی PDF
    html = HTML(string=html_string, base_url=settings.STATIC_ROOT)
    css = CSS(
        filename=css_path,
        font_config=None,
    )

    pdf_file = html.write_pdf(stylesheets=[css])

    # پاسخ HTTP جهت نمایش در مرورگر
    response = HttpResponse(pdf_file, content_type="application/pdf")
    filename = f"فاکتور_{invoice.invoice_number}.pdf"
    response["Content-Disposition"] = f"inline; filename={filename}"
    return response
