from django.db import models
# import json

# Create your models here.


class KoreanRecipe(models.Model):
    # blank allows an empty string and null means nullable in the db column
    # when user is deleted, this user field turns into None

    # original columns in csv
    # RCP_SEQ, RCP_NM, RCP_WAY2, RCP_PAT2, INFO_WGT, INFO_ENG, INFO_CAR,
    # INFO_PRO, INFO_FAT, INFO_NA, HASH_TAG, ATT_FILE_NO_MAIN, ATT_FILE_NO_MK,
    # RCP_PARTS_DTLS, MANUAL01, MANUAL_IMG01, MANUAL02, MANUAL_IMG02,
    # MANUAL03, MANUAL_IMG03, MANUAL04, MANUAL_IMG04, MANUAL05, MANUAL_IMG05,
    # MANUAL06, MANUAL_IMG06, RAW, parsed
    # 일련번호, 메뉴명, 조리방법, 요리종류, 중량(1인분), 열량, 탄수화물,
    # 단백질, 지방, 나트륨, 해쉬태그, 이미지경로(소), 이미지경로(대),
    # 재료정보, 만드는법_01, 만드는법_이미지_01, 만드는법_02, 만드는법_이미지_02,
    # 만드는법_03, 만드는법_이미지_03, 만드는법_04, 만드는법_이미지_04, 만드는법_05, 만드는법_이미지_05,
    # 만드는법_06, 만드는법_이미지_06, 재료 정보 파싱 리스트(계량 포함), 재료 핵심어 리스트(파싱 후)

    rcp_seq = models.IntegerField() # 일련번호(식약처db idx)
    rcp_nm = models.CharField(max_length=200)
    rcp_way2 = models.CharField(max_length=100, blank=True, null=True)
    rcp_pat2 = models.CharField(max_length=100, blank=True, null=True)
    info_wgt = models.FloatField(blank=True, null=True)
    info_eng = models.FloatField(blank=True, null=True)
    info_car = models.FloatField(blank=True, null=True)
    info_pro = models.FloatField(blank=True, null=True)
    info_fat = models.FloatField(blank=True, null=True)
    info_na = models.FloatField(blank=True, null=True)
    hash_tag = models.CharField(max_length=100, blank=True, null=True)
    att_file_no_main = models.CharField(max_length=500, blank=True, null=True) # 이미지경로(소)
    att_file_no_mk = models.CharField(max_length=500, blank=True, null=True) # 이미지경로(대)
    rcp_parts_dtls = models.CharField(max_length=500, blank=True, null=True) # 재료정보

    manual01 = models.CharField(max_length=500, blank=True, null=True)
    manual_img01 = models.CharField(max_length=500, blank=True, null=True)
    manual02 = models.CharField(max_length=500, blank=True, null=True)
    manual_img02 = models.CharField(max_length=500, blank=True, null=True)
    manual03 = models.CharField(max_length=500, blank=True, null=True)
    manual_img03 = models.CharField(max_length=500, blank=True, null=True)
    manual04 = models.CharField(max_length=500, blank=True, null=True)
    manual_img04 = models.CharField(max_length=500, blank=True, null=True)
    manual05 = models.CharField(max_length=500, blank=True, null=True)
    manual_img05 = models.CharField(max_length=500, blank=True, null=True)
    manual06 = models.CharField(max_length=500, blank=True, null=True)
    manual_img06 = models.CharField(max_length=500, blank=True, null=True)

    raw = models.CharField(max_length=500, blank=True, null=True) # 재료 정보 파싱 리스트(계량 포함)
    parsed = models.CharField(max_length=500, blank=True, null=True) # 재료 핵심어 리스트(파싱 후)

    objects = models.Manager()

    # class Meta:
    #     # db_table = 'news'
    #     managed = False  # 이걸 잠깐 추가해줍니다.


