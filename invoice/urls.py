# invoice/urls.py
from django.urls import path
from .views import generate_invoice_pdf

urlpatterns = [
    path("pdf/<int:pk>/", generate_invoice_pdf, name="invoice-pdf"),
]
