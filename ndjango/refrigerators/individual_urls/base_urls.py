from django.urls import path, include
from refrigerators.views import base_crud, photo_insert
from refrigerators.individual_urls.photo_urls import urlpatterns as photo_urls

'''
수기 입력 및 CRUD 모듈 + 알림 모듈
'''

urlpatterns = [
    path('', base_crud.index, name="index"),
    path('register/', include(photo_urls)),
    path('register/', base_crud.insertion_method, name='insertion_method'),
    path('register/manual/', base_crud.register_manual, name='register_manual'),
    path('register/barcode/', base_crud.register_barcode, name='register_barcode'),
    path('edit/<int:pk>/', base_crud.edit, name='edit'),
    path('view/<int:pk>/', base_crud.view, name='view'),
    path('delete/<int:pk>/', base_crud.delete, name='delete'),
    path('media/<int:pk>/', base_crud.serve_grocery_image, name='image'),
    path('expiring/', base_crud.expiring_groceries, name='expiring'),
]