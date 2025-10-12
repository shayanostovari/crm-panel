import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.views import View
from .models import Invoice


class InvoicePDFView(View):
    def get(self, request, pk):
        try:
            # گرفتن شیء فاکتور از دیتابیس
            obj = Invoice.objects.get(pk=pk)

            # ساخت مسیرهای مطلق استاتیک برای لیارا
            logo_path = os.path.join(settings.STATIC_ROOT, 'invoice/pics/logo.jpg')
            telegram_path = os.path.join(settings.STATIC_ROOT, 'invoice/pics/icons8-telegram-24.png')
            msg_path = os.path.join(settings.STATIC_ROOT, 'invoice/pics/icons8-message-50.png')
            phone_path = os.path.join(settings.STATIC_ROOT, 'invoice/pics/icons8-phone-50.png')

            # آماده‌سازی context برای قالب HTML
            context = {
                'object': obj,
                'business_name': obj.business_name,
                'agency_manager': obj.agency_manager,
                'total_amount': obj.total_amount(),
                'logo_data': logo_path,
                'telegram_icon': telegram_path,
                'msg_icon': msg_path,
                'phone_icon': phone_path,
                # در صورت داشتن اطلاعات اضافی:
                'description': getattr(obj, 'description', ''),
            }

            # رندر قالب به HTML
            html_string = render_to_string('invoice/invoice_template.html', context)

            # تبدیل HTML به PDF با WeasyPrint
            html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
            pdf_file = html.write_pdf()

            # پاسخ HTTP با فایل PDF
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'filename="invoice_{obj.pk}.pdf"'
            return response

        except Exception as e:
            # خطاگیری برای اشکال‌یابی در لیارا
            return HttpResponse(f"PDF generation failed: {str(e)}")
