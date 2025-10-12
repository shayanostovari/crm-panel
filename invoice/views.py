# invoice/views.py
from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from django.http import HttpResponse
import traceback
from .models import Invoice


class InvoicePDFView(WeasyTemplateResponseMixin, DetailView):
    model = Invoice
    template_name = 'invoice/invoice_template.html'
    pdf_filename = 'invoice.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        context.update({
            'invoice': obj,
            'object': obj,
            # اطلاعات ثابت شرکت
            'company_name': 'کانون آگهی و تبلیغات بازارسازان هوشمند پویا',
            'company_address': 'تهران، کیلومتر ۱۴ جاده مخصوص کرج...',
            'company_phone': '۴۴۷۸۲۳۵۱ - ۴۴۷۸۰۱۵۶',
            # فیلدهای واقعی مدل فاکتور
            'business_name': obj.business_name,
            'agency_manager': obj.agency_manager,
            'total_price': obj.total_amount(),  # تابع محاسبه مجموع کل از مدل
        })
        return context

    def get(self, request, *args, **kwargs):
        """هندل خطاها برای مشاهده‌ی traceback در صورت ارور ۵۰۰"""
        try:
            return super().get(request, *args, **kwargs)
        except Exception:
            return HttpResponse(
                traceback.format_exc(),
                content_type="text/plain",
                status=500
            )
