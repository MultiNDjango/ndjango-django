from django.urls import path, include
from . import views

'''
메인 홈페이지
'''

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('contact/', views.contact, name="contact"),
]