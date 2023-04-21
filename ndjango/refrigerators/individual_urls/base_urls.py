from django.urls import path
from refrigerators.views import base_crud

'''
수기 입력 및 CRUD 모듈 + 알림 모듈
'''

urlpatterns = [
    path('', base_crud.index, name="index"),
    path('register/', base_crud.register, name='register'),
    path('edit/<int:pk>/', base_crud.edit, name='edit'),
    path('view/<int:pk>/', base_crud.view, name='view'),
    path('delete/<int:pk>/', base_crud.delete, name='delete'),
    path('media/<int:pk>/<str:filename>/', base_crud.serve_grocery_image, name='image'),
]