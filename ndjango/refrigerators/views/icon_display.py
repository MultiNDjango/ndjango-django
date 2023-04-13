from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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


def fridge(request):
    payment_data={}
    if request.method == 'POST':
        var = request.POST['body']
        payment_data = json.loads(request.body)
        here = 0


    # a = request.data.get('fridge')
    # print(a)

    return JsonResponse({'ok': payment_data})


