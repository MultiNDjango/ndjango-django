from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
# from rest_framework.renderers import JSONRenderer

from refrigerators.models import Location, Grocery
from refrigerators.serializers import LocationSerializer
from refrigerators.serializers import GrocerySerializer
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_protect

'''
냉장고 식재료 위치 제어 모듈
'''


def view_d(request):
    return HttpResponse('homepage')


def get_init_val():
    return {"냉동": [
                    {1: None, 2: None, 3: None, 4: None, 5: None},
                    {1: None, 2: None, 3: None, 4: None, 5: None},
                    {1: None, 2: None, 3: None, 4: None, 5: None},
                    {1: None, 2: None, 3: None, 4: None, 5: None},
                    {1: None, 2: None, 3: None, 4: None, 5: None}
                ],
                "냉장": [
                    {1: None, 2: None, 3: None, 4: None, 5: None},
                    {1: None, 2: None, 3: None, 4: None, 5: None},
                    {1: None, 2: None, 3: None, 4: None, 5: None},
                    {1: None, 2: None, 3: None, 4: None, 5: None},
                    {1: None, 2: None, 3: None, 4: None, 5: None},
                    {1: None, 2: None, 3: None, 4: None, 5: None},
                    {1: None, 2: None, 3: None, 4: None, 5: None}
                ]}


@api_view(['GET', 'PATCH'])
@parser_classes([JSONParser])
def two_doors(request):
    context = {}

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return Response({'msg': 'login required'}, status=status.HTTP_400_BAD_REQUEST)

        current_user = request.user
        location = Location.objects.get(user=current_user.id)
        if not location.location:
            init_dict = get_init_val()
            location = Location.objects.get(user=current_user.id)
            location.location = init_dict
            location.save()

        # load location
        location_serializer = LocationSerializer(location)
        fridge = location_serializer.data
        fridge_dict = dict(fridge)

        # filter ids only
        dict_fresh_ice = []
        [[dict_fresh_ice.append(int(v)) for _, v in dict_fi.items() if v] for dict_fi in fridge_dict['location']['냉동']]
        [[dict_fresh_ice.append(int(v)) for _, v in dict_fi.items() if v] for dict_fi in fridge_dict['location']['냉장']]
        # print(dict_fresh_ice) # [1, 2]

        # grocery dict
        grocery_info = Grocery.objects.filter(pk__in=dict_fresh_ice)
        grocery_serializer = GrocerySerializer(grocery_info, many=True)
        grocery_data = grocery_serializer.data
        grocery_dict = {}
        for grc in grocery_data:
            cur_id = str(grc['id'])
            grocery_dict[cur_id] = {
                'id': int(grc['id']),
                'name': grc['name'],
                'category': grc['category'],
                'qty': grc['qty'],
                'in_date': grc['in_date'],
                'exp_date': grc['exp_date'],
                'str': f"이름: {grc['name']}, 카테고리: {grc['category']}, 수량: {grc['qty']}, 입고일: {grc['in_date']}, 소비기한: {grc['exp_date']}"
            }


        tmp = fridge['location']['냉동']

        def get_grocery_details(primary_keys: list) -> list:
            details = list()
            for row in primary_keys:
                cells = dict()
                for k, v in row.items():
                    if not v:
                        cells[k] = None
                        continue

                    cells[k] = grocery_dict[v]

                details.append(cells)
            return details

        # combine dicts
        ice = get_grocery_details(fridge['location']['냉동'])
        fresh = get_grocery_details(fridge['location']['냉장'])

        # ice = list()
        # for row in fridge['location']['냉동']:
        #     print(row)
        #     cells = dict()
        #     for key, val in row.items():
        #         print(key, val)
        #         if not val:
        #             cells[key] = None
        #             continue
        #
        #         cells[key] = grocery_dict[key]
        #
        #     ice.append(cells)
        #
        # fresh = list()
        # for row in fridge['location']['냉장']:
        #     print(row)
        #     cells = dict()
        #     for key, val in row.items():
        #         print(key, val)
        #         if not val:
        #             cells[key] = None
        #             continue
        #
        #         cells[key] = grocery_dict[key]
        #
        #     fresh.append(cells)

        # context filler
        # context['ice'] = fridge['location']['냉동']
        # context['fresh'] = fridge['location']['냉장']
        # context['loc_detail'] = grocery_dict
        context['ice'] = ice
        context['fresh'] = fresh

        return render(request, 'refrigerators/two_doors.html', context)

    elif request.method == 'PATCH':
        return Response({'msg': 'currently unavailable'}, status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({'msg': 'currently unavailable'})


# ignore foreign key constrains
# https://stackoverflow.com/questions/10623854/django-soft-foreignfield-without-database-integrity-checks/11926432#11926432


@api_view(['POST', 'PATCH'])
@parser_classes([JSONParser])
def loc_patch(request, user):
    if request.method == 'PATCH':
        data = JSONParser().parse(request)
        location = Location.objects.get(user=user)
        location.location = data['location']
        location.save()

        return JsonResponse({'location': data['location']})






