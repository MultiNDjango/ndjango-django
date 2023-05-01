from django.urls import path, include
from refrigerators.views import barcode_insert

'''
바코드 입력 모듈
'''

urlpatterns = [
    path('a', barcode_insert.view_a, name="view_a"),
]