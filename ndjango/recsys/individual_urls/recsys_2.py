from django.urls import path, include
from recsys.views import recsys_2

'''
추천시스템 2 모듈
'''

urlpatterns = [
    path('', recsys_2.korean_recipes, name="korean_recipes"),
    path('<int:recipe>', recsys_2.kor_recipe_detail, name="kor_recipe_detail"),
]