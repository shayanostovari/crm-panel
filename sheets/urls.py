from django.urls import path
from . import views

urlpatterns = [
    path("", views.hamti_list, name="hamti_list"),
    path("<int:pk>/", views.hamti_detail, name="hamti_detail"),
]
