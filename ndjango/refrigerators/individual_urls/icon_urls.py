from django.urls import path, include
from refrigerators.views import icon_display

'''
냉장고 식재료 위치 제어 모듈
'''

urlpatterns = [
    path('d', icon_display.view_d, name="view_d"),
    path('icons', icon_display.icon_view, name="icon_view"),
    path('two-doors', icon_display.ref_view, name="two_doors"),
    path('two-doors/fridge', icon_display.fridge, name="fridge"),
]