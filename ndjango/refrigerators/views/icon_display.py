from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_protect
import json

'''
냉장고 식재료 위치 제어 모듈
'''


def view_d(request):
    return HttpResponse('homepage')


def icon_view(request):
    return render(request, 'refrigerators/icon.html')


def ref_view(request):
    context = {
        "foods": [
            ['족발', '', '햄버거', '초밥', ''],
            ['', '피자', '', '', ''],
            ['족발', '', '', '초밥', ''],
            ['', '피자', '햄버거', '', ''],
            ['', '', '햄버거', '', ''],
        ]
    }

    return render(request, 'refrigerators/two_doors.html', context)


# @csrf_exempt
@api_view(['POST'])
def fridge(request):

    if request.method == 'POST':
        var = request.data

    return JsonResponse({'ok': var})


