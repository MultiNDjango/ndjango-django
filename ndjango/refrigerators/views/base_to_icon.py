from refrigerators.serializers import LocationSerializer, IconSerializer, GrocerySerializer
from refrigerators.models import Location, Icon, Grocery
from django.core.exceptions import ObjectDoesNotExist

from refrigerators.views.icon_display import load_fridge_location

'''
식재료 등록/삭제 후 냉장고 icon(location)과 연동하는 모듈
'''


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


def set_grocery_location(grocery_pk, user_pk):
    # load user location
    try:
        location = Location.objects.get(user=user_pk)
    except ObjectDoesNotExist:
        location = initialize_location(user_pk)

    if not location.location:
        location = initialize_location(user_pk, True)

    location_serializer = LocationSerializer(location)

    # insert new grocery in a null cell
    rst_instance = location_serializer.auto_locate_by_grocery_id(location_serializer.instance, grocery_pk)

    if not rst_instance:
        print("fridge is full")
        return None

    return rst_instance


def remove_grocery_location(grocery_pk, user_pk):
    # load user location
    location = Location.objects.get(user=user_pk)
    if not location.location:
        location = initialize_location(user_pk)
        print("location is initialized since it didn't exist")
        return None

    location_serializer = LocationSerializer(location)
    # remove selected grocery from the cell accordingly
    rst_instance = location_serializer.delete_by_grocery_id(location_serializer.instance, grocery_pk)

    if not rst_instance:
        print("selected grocery doesn't exist in fridge")
        return None

    return rst_instance



def get_fridge_location_info(user):
    current_user = user

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

    return ice, fresh
