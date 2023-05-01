from refrigerators.serializers import LocationSerializer
from refrigerators.models import Location
from django.core.exceptions import ObjectDoesNotExist

'''
식재료 등록/삭제 후 냉장고 icon(location)과 연동하는 모듈
'''


def initialize_location(user_pk, if_init=False):
    # record already exist with Null value
    if if_init:
        location = Location.objects.get(user=user_pk)
        location.location = LocationSerializer.init_dict
        # location.location = init_dict
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


