# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 19:34:04 2023

@author: PC
"""
#사용한 모듈
import pandas as pd
import re
import ast
import pickle
from collections import Counter, defaultdict
from django.shortcuts import render

#처리된 레시피 데이터 호출
enrecipe_cleaned=pd.read_csv('../data/data_eng_recipe/enrecipe_cleanedver2.csv')
#한-영 카테고리 키워드 데이터 호출
t3_keys=pd.read_csv('../data/data_eng_recipe/t3_categories.csv',encoding='utf-8')
#기본 지정 임계치 설정
threshold=0.1
# 카테고리 데이터 호출
with open('../data/data_eng_recipe/spectralingre23.pickle', 'rb') as handle:
    ing_categories = pickle.load(handle)

key3_dict=dict([(kor,eng) for kor,eng in zip(t3_keys['kor'], t3_keys['eng'])])

    
def search_recipes(ing_list, threshold=0.2, ing_categories=ing_categories,dictkeys=key3_dict,enrecipe_cleaned=enrecipe_cleaned):
    result = []
    en_ing_list = []
    for korean_ing in ing_list:
        en_ing_keys = key3_dict.get(korean_ing)
        
        if ing_categories.get(en_ing_keys) is not None:
            en_ing_list.append(key3_dict.get(korean_ing))
            ing_list.remove(korean_ing)
    en_ing_list.extend(ing_list)
    
        

    for i, recipe in enrecipe_cleaned.iterrows():
        # Check if recipe contains at least one ingredient from the input list
        ingredients = ast.literal_eval(recipe['Ingredients'])
        matches = [ing for ing in en_ing_list if any(re.search(rf'\b{ing}\b', ingredient, flags=re.IGNORECASE) for ingredient in ingredients)]
        if not matches:
            
            continue
        
        # Calculate match percentage
        ing_count = len(en_ing_list)
        search_ing=[]
        search_count = 0
        for ingredient in ingredients:
            for ing in en_ing_list:
                if re.search(rf'\b{ing}\b', ingredient, flags=re.IGNORECASE):
                    if ing in search_ing:
                        pass
                    else:
                        search_ing.append(ing)
                        search_count += 1
                    break
        match_percentage = search_count / ing_count * 100
        
        # Check if match percentage exceeds the threshold
        if match_percentage >= threshold:
            # Check if all ingredients from the input list are present
            search_count = 0
            search_ing_list=[]
            for ingredient in ingredients:
                for ing in en_ing_list:
                    if re.search(rf'\b{ing}\b', ingredient, flags=re.IGNORECASE):
                        if ing in search_ing_list:
                            pass
                        else:
                            search_count += 1
                            search_ing_list.append(ing)
                        break
            if search_count/ing_count > threshold:
                result.append([i,match_percentage])
    sorted_result = sorted(result, key=lambda x: x[1], reverse=True)
    return sorted_result


def get_index(idx):
    matchesidx=[]
    for i in range(len(idx)):
        matchesidx.append(idx[i][0])
    return matchesidx
### 실행 코드


# index에 맞춰 필요한 데이터 호출
#t=enrecipe_cleaned.loc[get_index(search_recipes(list(input('재료를 입력하세요:').split(',')))),['Title','Instructions','Image_Name','Cleaned_Ingredients']]
'''
def get_recipe_info(request):
    message = request.GET.get('message')
    recinfo = enrecipe_cleaned.loc[get_index(search_recipes(message)),['Title','Instructions','Image_Name','Cleaned_Ingredients','Clean_Ing']][0:10]
    info3=[]
    for i in range(len(recinfo)):
        series1=list(recinfo['Instructions'])[i].split('\n')
        series2=eval(list(recinfo['Cleaned_Ingredients'])[i])
        info3.append([series1,series2])
    return 
'''     
#recinfo = enrecipe_cleaned.loc[get_index(search_recipes(input('재료입력:'))),['Title','Instructions','Image_Name','Cleaned_Ingredients','Clean_Ing']][0:10]


