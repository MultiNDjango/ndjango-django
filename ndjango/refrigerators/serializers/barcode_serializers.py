from rest_framework import serializers
from refrigerators.models.barcode_models import Icon


class IconSerializer(serializers.ModelSerializer):

    class Meta:
        model = Icon
        fields = ['category', 're_category', 'icon_img']

    @staticmethod
    def get_icon_dict(serializer_data):

        icon_dict = dict()

        for icon in serializer_data:
            key = icon['category']
            icon_dict[key] = {
                're_category': icon['re_category'],
                'icon_img': icon['icon_img']
            }

        return icon_dict

