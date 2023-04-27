from rest_framework import serializers
from recsys.models.recsys_2_models import KoreanRecipe


class KoreanRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = KoreanRecipe
        fields = '__all__'



