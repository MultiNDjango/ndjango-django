from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    choices = (
                  ('nuts', '땅콩'),
                  ('seafood', '해산물'),
                  ('eggs', '달걀'),
                  ('bean', '콩'),
                  ('wheat', '밀'),
                  ('milk', '우유'),
                  ('mackerel', '고등어'),
                  ('crab', '게'),
                  ('shirimp', '새우'),
                  ('pork', '돼지고기'),
                  ('peach', '복숭아'),
                  ('tomato', '토마토'),
                  ('walnut', '호두'),
                  ('chicken', '닭고기'),
                  ('pork', '쇠고기'),
                  ('squid', '오징어'),
                  ('oyster', '굴'),
              )

    choices_dict = dict((x, y) for x, y in choices)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def allergy_in_korean(self):
        cur_instance = self.instance
        allergy_eng = cur_instance.allergy['allergy'] if cur_instance.allergy else []
        allergy_kor = [self.choices_dict[item] for item in allergy_eng]
        return allergy_kor





# from rest_framework import serializers
# from django.contrib.auth.models import User
#
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')
#
#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         return user