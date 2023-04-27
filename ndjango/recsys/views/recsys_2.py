from django.shortcuts import render
# from django.http import HttpResponse
# from django.http import JsonResponse
# import json
# import requests
import asyncio
import httpx

'''
추천시스템 2 모듈
'''


def get_recipes(request):
    url = '127.0.0.1:5000/recipes'

    recipes_total = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추', '양파', '마늘', '돼지고기']))
    recipes_veges = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추', '양파', '마늘']))
    recipes_allergy = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추', '양파']))
    recipes_calorie = asyncio.run(async_get_recipes(url, ['감자', '대파', '부추']))

    context = {
        'total': recipes_total,
        'veges': recipes_veges,
        'allergy': recipes_allergy,
        'calorie': recipes_calorie,
        'n': range(5),
    }






    return render(request, 'recsys_2/kor_index.html', context)


async def async_get_recipes(url, sample_list=['대파', '부추'], n=10):
    ingredients = ','.join(sample_list)
    url = f'http://{url}?ingredients={ingredients}&n={n}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

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
