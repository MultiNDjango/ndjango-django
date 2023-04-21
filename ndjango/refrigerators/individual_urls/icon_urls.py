from django.urls import path, include
from refrigerators.views import icon_display

'''
냉장고 식재료 위치 제어 모듈
'''

urlpatterns = [
    path('d', icon_display.view_d, name="view_d"),
    path('', icon_display.two_doors, name="two_doors"),
    path('<int:user>', icon_display.loc_patch, name="loc_patch"),
]