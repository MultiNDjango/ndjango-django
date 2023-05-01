from rest_framework import serializers
from refrigerators.models.icon_models import Location


class LocationSerializer(serializers.ModelSerializer):
    # user = serializers.IntegerField(required=False, allow_blank=True)
    # location = serializers.JSONField(required=False, allow_blank=True)

    init_dict = {"냉동": [
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

    class Meta:
        model = Location
        fields = ['user', 'location']

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance

    @staticmethod
    def place_grocery(section: list, new_pk: int) -> list:
        modified_fresh_or_ice = section
        if_set = False

        for idx, row in enumerate(section):
            if if_set:
                break

            for key_num, v in row.items():
                if not v:
                    modified_fresh_or_ice[idx][key_num] = str(new_pk)
                    if_set = True
                    break

                else:
                    continue

        return if_set, modified_fresh_or_ice

    def auto_locate_by_grocery_id(self, instance, new_grocery_pk):
        initial_location = instance.location

        # place new grocery id in a null cell
        initial_fresh = initial_location['냉장']
        initial_ice = initial_location['냉동']

        if_set, modified_fresh = self.place_grocery(initial_fresh, new_grocery_pk)
        if not if_set:
            if_set, modified_ice = self.place_grocery(initial_ice, new_grocery_pk)

            # in case of fully filled fridge
            if not if_set:
                return None

            # when the new grocery was placed in the ice section
            instance.location['냉동'] = modified_ice
            instance.save()
            return instance

        # when the new grocery was placed in the fresh section
        instance.location['냉장'] = modified_fresh
        instance.save()
        return instance

    @staticmethod
    def remove_grocery(section: list, grocery_pk: int) -> list:
        modified_fresh_or_ice = section
        grocery_pk = str(grocery_pk)
        if_set = False

        for idx, row in enumerate(section):
            if if_set:
                break

            for key_num, v in row.items():
                if v == grocery_pk:
                    modified_fresh_or_ice[idx][key_num] = None
                    if_set = True
                    break

                else:
                    continue

        return if_set, modified_fresh_or_ice

    def delete_by_grocery_id(self, instance, grocery_pk):
        initial_location = instance.location

        # iterate fridge sections to remove grocery
        initial_fresh = initial_location['냉장']
        initial_ice = initial_location['냉동']

        if_set, modified_fresh = self.remove_grocery(initial_fresh, grocery_pk)

        if not if_set:
            if_set, modified_ice = self.remove_grocery(initial_ice, grocery_pk)

            # if the grocery doesn't exist in fridge
            if not if_set:
                return None

            # when the new grocery was removed in the ice section
            instance.location['냉동'] = modified_ice
            instance.save()
            return instance

        # when the new grocery was placed in the fresh section
        instance.location['냉장'] = modified_fresh
        instance.save()
        return instance



    # def update(self, instance, validated_data):
    #     for (key, value) in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     return instance

