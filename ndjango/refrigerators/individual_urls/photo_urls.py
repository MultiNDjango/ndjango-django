from django.urls import path, include
from refrigerators.views import photo_insert

'''
음식 사진 입력 모듈
'''

# 객체 검출 모델 및 추론 모듈은 별도의 restAPI 서버에 구현 후 api call을 통해 output만 받아서 화면에 디스플레이 하기

urlpatterns = [
    path('upload/', photo_insert.photo_upload, name="photo_upload"),
]
