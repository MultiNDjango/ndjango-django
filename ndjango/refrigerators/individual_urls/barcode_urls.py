from django.urls import path
from refrigerators import views

urlpatterns = [
    path('', views.search_barcode, name='search_barcode'),
    path('barcode_info/<barcode>/', views.barcode_info, name='barcode_info'),
]

