from django.urls import path,include
from recsys.views import recsys_1

'''
추천시스템 1 모듈
'''

urlpatterns= [
    path('',recsys_1.eng_search, name="eng_recipes_input"),
    path('eng_result/',recsys_1.get_recipe_info, name="eng-recipes-result"),
]
