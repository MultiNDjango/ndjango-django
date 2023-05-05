from django.shortcuts import render
# from django.http import HttpResponse
# from django.http import JsonResponse
# import json
# import requests
import asyncio
import httpx
import random
import datetime

from recsys.models import KoreanRecipe
from recsys.serializers import KoreanRecipeThumbnailSerializer
from recsys.serializers import KoreanRecipeSerializer

from refrigerators.models import Grocery
from refrigerators.serializers import GrocerySerializer
from users.models import CustomUser
from users.serializer import CustomUserSerializer

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

    # if not request.user.is_authenticated:
    #     pass

    # user's grocery lists
    user_pk = request.user.id
    grocery_info = Grocery.objects.filter(userid=user_pk)
    grocery_serializer = GrocerySerializer(grocery_info, many=True)
    grocery_data = grocery_serializer.data

    # items to infer
    grc_whole = [item['name'] for item in grocery_data]
    grc_veges = [item['name'] for item in grocery_data if item['category'] == 'vegetable']
    grc_fruit = [item['name'] for item in grocery_data if item['category'] == 'fruit']
    grc_expiring = []
    # groceries expiring within 5 days
    limit_date = datetime.datetime.now() + datetime.timedelta(days=5)
    for item in grocery_data:
        exp_date = datetime.datetime.strptime(item['exp_date'], '%Y-%m-%d')
        sub = limit_date - exp_date
        if datetime.timedelta(days=0) <= sub <= datetime.timedelta(days=6):
            grc_expiring.append(item['name'])

    # user's allergy info
    user_info = CustomUser.objects.get(id=user_pk)
    user_serializer = CustomUserSerializer(user_info)
    grc_allergy = user_serializer.allergy_in_korean()

    # get recipes through async api calls
    recipes_whole = asyncio.run(async_get_recipes(url, grc_whole))
    recipes_veges = asyncio.run(async_get_recipes(url, grc_veges))
    recipes_expiring = asyncio.run(async_get_recipes(url, grc_expiring))
    # fruit first but if there's no fruits, any of the whole groceries
    try:
        fruit = random.choice(grc_fruit)
        recipes_fruit = asyncio.run(async_get_recipes(url, fruit))
    except IndexError:
        rand = random.choices(grc_whole)
        rand_name = rand[0]
        recipes_random = asyncio.run(async_get_recipes(url, rand))
    recipes_allergy = asyncio.run(async_get_recipes_with_allergy(url, grc_whole, grc_allergy))

    # restructure recipes
    whole = get_sorted_recipe_thumbnail(recipes_whole)
    veges = get_sorted_recipe_thumbnail(recipes_veges)

    try:
        fruits = get_sorted_recipe_thumbnail(recipes_fruit)

    except UnboundLocalError:
        rands = get_sorted_recipe_thumbnail(recipes_random)
    allergy = get_sorted_recipe_thumbnail(recipes_allergy)
    expiring = get_sorted_recipe_thumbnail(recipes_expiring)

    context = {
        'whole': whole,
        'veges': veges,
        'allergy': allergy,
        'expiring': expiring,
        'whole_list': ", ".join(grc_whole),
        'veges_list': ", ".join(grc_veges),
        'allergy_list': ", ".join(grc_allergy),
        'expiring_list': ", ".join(grc_expiring)
    }
    try:
        context['fruits'] = fruits
    except UnboundLocalError:
        context['rands'] = rands

    return render(request, 'recsys_2/kor_index.html', context)


async def async_get_recipes(url, grocery=['대파', '부추'], n=10):
    ingredients = ','.join(grocery)
    url = f'http://{url}?ingredients={ingredients}&n={n}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


async def async_get_recipes_with_allergy(url, to_include=['대파', '부추'], to_remove=[], n=10):
    ingredients = ','.join(to_include)
    allergies = ','.join(to_remove)
    url = f'http://{url}-allergy?ingredients={ingredients}&allergies={allergies}&n={n}'

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
