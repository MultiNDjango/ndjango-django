from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
# from rest_framework.renderers import JSONRenderer

from refrigerators.models import Location
from refrigerators.models import Grocery
from refrigerators.models import Icon
from refrigerators.serializers import LocationSerializer
from refrigerators.serializers import GrocerySerializer
from refrigerators.serializers import IconSerializer
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist

'''
냉장고 식재료 위치 제어 모듈
'''


def view_d(request):
    # sample test
    return HttpResponse('homepage')


def initialize_location(user_pk, if_init=False):
    # record already exist with Null value
    if if_init:
        location = Location.objects.get(user=user_pk)
        location.location = LocationSerializer.init_dict
        location.save()
        return location

    # create new location instance
    data_dict = {
        'user': user_pk,
        'location': LocationSerializer.init_dict
    }

    serializer = LocationSerializer(data=data_dict)
    if serializer.is_valid():
        serializer.save()
        location = Location.objects.get(user=user_pk)

    return location


def load_fridge_location(user_pk):
    # load user location
    try:
        location = Location.objects.get(user=user_pk)
    except ObjectDoesNotExist:
        location = initialize_location(user_pk)

    if not location.location:
        location = initialize_location(user_pk, True)

    return location


@api_view(['GET', 'PATCH'])
@parser_classes([JSONParser])
def two_doors(request):
    context = {}

    if request.method == 'GET':
        if not request.user.is_authenticated:
            return Response({'msg': 'login required'}, status=status.HTTP_400_BAD_REQUEST)

        current_user = request.user

        # load location
        location = load_fridge_location(current_user.id)
        location_serializer = LocationSerializer(location)
        fridge = location_serializer.data
        fridge_dict = dict(fridge)

        # filter ids only
        dict_fresh_ice = []
        [[dict_fresh_ice.append(int(v)) for _, v in dict_fi.items() if v] for dict_fi in fridge_dict['location']['냉동']]
        [[dict_fresh_ice.append(int(v)) for _, v in dict_fi.items() if v] for dict_fi in fridge_dict['location']['냉장']]
        # print(dict_fresh_ice) # [1, 2]

        # load icon dict
        icon_imgs = Icon.objects.all()
        icon_serializer = IconSerializer(icon_imgs, many=True)
        icon_data = icon_serializer.data
        icon_dict = IconSerializer.get_icon_dict(icon_data)

        # restructure grocery dict
        grocery_info = Grocery.objects.filter(pk__in=dict_fresh_ice)
        grocery_serializer = GrocerySerializer(grocery_info, many=True)
        grocery_data = grocery_serializer.data
        grocery_dict = {}
        for grc in grocery_data:
            re_category = icon_dict[grc['category']]['re_category']
            icon_img = icon_dict[grc['category']]['icon_img']
            cur_id = str(grc['id'])
            grocery_dict[cur_id] = {
                'id': int(grc['id']),
                'name': grc['name'],
                'category': grc['category'],
                're_category': re_category,
                'qty': grc['qty'],
                'in_date': grc['in_date'],
                'exp_date': grc['exp_date'],
                'icon_img': icon_img,
                'str': f"이름: {grc['name']}, 카테고리: {re_category}, 수량: {grc['qty']}, 입고일: {grc['in_date']}, 소비기한: {grc['exp_date']}"
            }

        # tmp = fridge['location']['냉동']

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

        context['ice'] = ice
        context['fresh'] = fresh

        return render(request, 'refrigerators/two_doors.html', context)

    elif request.method == 'PATCH':
        return Response({'msg': 'currently unavailable'}, status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({'msg': 'currently unavailable'})


@api_view(['POST', 'PATCH'])
@parser_classes([JSONParser])
def loc_patch(request, user):
    if request.method == 'PATCH':
        data = JSONParser().parse(request)
        location = Location.objects.get(user=user)
        location.location = data['location']
        location.save()

        return JsonResponse({'location': data['location']})


# def get_fridge_location_info(user):
#     current_user = user
#
#     # load location
#     location = load_fridge_location(current_user.id)
#     location_serializer = LocationSerializer(location)
#     fridge = location_serializer.data
#     fridge_dict = dict(fridge)
#
#     # filter ids only
#     dict_fresh_ice = []
#     [[dict_fresh_ice.append(int(v)) for _, v in dict_fi.items() if v] for dict_fi in fridge_dict['location']['냉동']]
#     [[dict_fresh_ice.append(int(v)) for _, v in dict_fi.items() if v] for dict_fi in fridge_dict['location']['냉장']]
#     # print(dict_fresh_ice) # [1, 2]
#
#     # load icon dict
#     icon_imgs = Icon.objects.all()
#     icon_serializer = IconSerializer(icon_imgs, many=True)
#     icon_data = icon_serializer.data
#     icon_dict = IconSerializer.get_icon_dict(icon_data)
#
#     # restructure grocery dict
#     grocery_info = Grocery.objects.filter(pk__in=dict_fresh_ice)
#     grocery_serializer = GrocerySerializer(grocery_info, many=True)
#     grocery_data = grocery_serializer.data
#     grocery_dict = {}
#     for grc in grocery_data:
#         re_category = icon_dict[grc['category']]['re_category']
#         icon_img = icon_dict[grc['category']]['icon_img']
#         cur_id = str(grc['id'])
#         grocery_dict[cur_id] = {
#             'id': int(grc['id']),
#             'name': grc['name'],
#             'category': grc['category'],
#             're_category': re_category,
#             'qty': grc['qty'],
#             'in_date': grc['in_date'],
#             'exp_date': grc['exp_date'],
#             'icon_img': icon_img,
#             'str': f"이름: {grc['name']}, 카테고리: {re_category}, 수량: {grc['qty']}, 입고일: {grc['in_date']}, 소비기한: {grc['exp_date']}"
#         }
#
#     # tmp = fridge['location']['냉동']
#
#     def get_grocery_details(primary_keys: list) -> list:
#         details = list()
#         for row in primary_keys:
#             cells = dict()
#             for k, v in row.items():
#                 if not v:
#                     cells[k] = None
#                     continue
#
#                 cells[k] = grocery_dict[v]
#
#             details.append(cells)
#         return details
#
#     # combine dicts
#     ice = get_grocery_details(fridge['location']['냉동'])
#     fresh = get_grocery_details(fridge['location']['냉장'])
#
#     return ice, fresh




# ignore foreign key constrains
# https://stackoverflow.com/questions/10623854/django-soft-foreignfield-without-database-integrity-checks/11926432#11926432

