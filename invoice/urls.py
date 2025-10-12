# invoice/urls.py
from django.urls import path
from .views import InvoicePDFView

urlpatterns = [
    path("pdf/<int:pk>/", InvoicePDFView.as_view(), name="invoice-pdf"),
]
