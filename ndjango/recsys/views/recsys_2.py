from django.shortcuts import render
# from django.http import HttpResponse
# from django.http import JsonResponse
# import json
# import requests
import asyncio
import httpx

from recsys.models import KoreanRecipe
from recsys.serializers import KoreanRecipeThumbnailSerializer
from recsys.serializers import KoreanRecipeSerializer

'''
추천시스템 2 모듈
'''

rcp_tmb_serializer = KoreanRecipeThumbnailSerializer()


def get_sorted_recipe_thumbnail(names):
    recipes = list(names['ingredients']['recipe'].values())
    recipe_info = KoreanRecipe.objects.filter(rcp_nm__in=recipes)
    info_val = KoreanRecipeThumbnailSerializer(recipe_info, many=True)
    sorted_recipe_thumbnail = rcp_tmb_serializer.sort_by_original_order(info_val, recipes)

    return sorted_recipe_thumbnail


def korean_recipes(request):
    url = '127.0.0.1:5000/recipes'

    recipes_total = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추', '양파', '마늘', '돼지고기']))
    recipes_veges = asyncio.run(async_get_recipes(url, ['애호박', '숙주']))
    recipes_allergy = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추', '양파']))
    recipes_calorie = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추']))

    # 여기부터 함수화
    # recipes_total_list = list(recipes_total['ingredients']['recipe'].values())
    #
    # # korean recipe
    # # recipe_info = KoreanRecipe.objects.values_list('id', 'rcp_nm', 'att_file_no_main').filter(rcp_nm__in=recipes_total_list)
    # recipe_info = KoreanRecipe.objects.filter(rcp_nm__in=recipes_total_list)
    # info_val = KoreanRecipeThumbnailSerializer(recipe_info, many=True)
    #
    #
    # sorted_recipe_thumbnails = rcp_tmb_serializer.sort_by_original_order(info_val, recipes_total_list)

    total = get_sorted_recipe_thumbnail(recipes_total)
    veges = get_sorted_recipe_thumbnail(recipes_veges)
    allergy = get_sorted_recipe_thumbnail(recipes_allergy)
    calorie = get_sorted_recipe_thumbnail(recipes_calorie)


    context = {
        # 'total': recipes_total,
        # 'veges': recipes_veges,
        # 'allergy': recipes_allergy,
        # 'calorie': recipes_calorie,
        'total': total,
        'veges': veges,
        'allergy': allergy,
        'calorie': calorie,
    }

    return render(request, 'recsys_2/kor_index.html', context)


async def async_get_recipes(url, sample_list=['대파', '부추'], n=10):
    ingredients = ','.join(sample_list)
    url = f'http://{url}?ingredients={ingredients}&n={n}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


def kor_recipe_detail(request, recipe):

    recipe_info = KoreanRecipe.objects.get(id=recipe)
    info_val = KoreanRecipeSerializer(recipe_info)

    cleansed_recipe_info = KoreanRecipeSerializer.restructure_process(info_val)

    context = {'recipe': cleansed_recipe_info}

    return render(request, 'recsys_2/kor_detail.html', context)

# def asyncio_run():
#     url = '127.0.0.1:5000/recipes'
#
#     import time
#     start = time.time()
#
#     resp = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추', '양파', '마늘', '돼지고기']))
#     print(resp.text)
#     end = time.time()
#     print(f"{end - start:.5f} sec")
#
#     resp = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추', '양파', '마늘']))
#     print(resp.text)
#     end = time.time()
#     print(f"{end - start:.5f} sec")
#
#     resp = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추', '양파']))
#     print(resp.text)
#     end = time.time()
#     print(f"{end - start:.5f} sec")
#
#     resp = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추']))
#     print(resp.text)
#     end = time.time()
#     print(f"{end - start:.5f} sec")


# if __name__ == '__main__':
#     asyncio_run()
