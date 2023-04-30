from rest_framework import serializers
from recsys.models.recsys_2_models import KoreanRecipe
from PIL import Image
import requests


class KoreanRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = KoreanRecipe
        fields = '__all__'

    @staticmethod
    def restructure_process(instance):
        initial_data = instance.data
        replaced_data = dict()

        # replace new lines
        for key, val in initial_data.items():
            if isinstance(val, str):
                initial_data[key] = val.replace('\n', ' ')

        # copy non-manual items
        for key, val in initial_data.items():
            if key[:6] == 'manual':
                break

            replaced_data[key] = val

        # restructure manual dict to list
        manuals_list = list()
        for i in range(1, 7):
            curr_manual_dict = dict()
            curr_manual_dict['instruction'] = initial_data[f"manual0{i}"]
            curr_manual_dict['image'] = initial_data[f"manual_img0{i}"]

            if not curr_manual_dict['instruction'] and not curr_manual_dict['image']:
                break

            manuals_list.append(curr_manual_dict)

        replaced_data['manual'] = manuals_list

        # replace smaller mk picture with main image
        main = Image.open(requests.get(replaced_data['att_file_no_main'], stream=True).raw)
        mk = Image.open(requests.get(replaced_data['att_file_no_mk'], stream=True).raw)

        main_w, main_h = main.size
        mk_w, mk_h = mk.size

        if main_h > mk_h:
            replaced_data['att_file_no_mk'] = replaced_data['att_file_no_main']

        return replaced_data


class KoreanRecipeThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = KoreanRecipe
        fields = ['id', 'rcp_nm', 'rcp_way2', 'rcp_pat2', 'att_file_no_main']

    @staticmethod
    def sort_by_original_order(instance, original: list) -> list:
        final_list = list()
        initial_data = instance.data

        for item in original:

            for val in initial_data:
                if val['rcp_nm'] == item:
                    final_list.append(val)
                    break

        return final_list





