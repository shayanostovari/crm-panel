from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from django.http import HttpResponse
import traceback
from .models import Invoice

# ---- نمایش فایل PDF فاکتور ----
class InvoicePDFView(WeasyTemplateResponseMixin, DetailView):
    model = Invoice
    template_name = 'invoice/invoice_template.html'
    pdf_filename = 'invoice.pdf'

    # فیلدهای context در قالب HTML
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        context.update({
            'invoice': obj,
            'object': obj,
            'company_name': 'کانون آگهی و تبلیغات بازارسازان هوشمند پویا',
            'company_address': 'تهران، کیلومتر ۱۴ جاده مخصوص کرج...',
            'company_phone': '۴۴۷۸۲۳۵۱ - ۴۴۷۸۰۱۵۶',
            'customer_name': obj.customer_name,
            'total_price': obj.total_price,
        })
        return context

    # هندل خطاها برای مشاهده‌ی Traceback در صورت ارور 500
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception:
            return HttpResponse(
                traceback.format_exc(), content_type="text/plain", status=500
            )
