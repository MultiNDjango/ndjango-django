from django.urls import path, include
from recsys.views import recsys_2

'''
추천시스템 2 모듈
'''

urlpatterns = [
    path('', recsys_2.get_recipes, name="rec-diet"),

]