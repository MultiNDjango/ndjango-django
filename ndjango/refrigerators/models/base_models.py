import datetime
from django.db import models
from users.models import CustomUser
# from django.conf import settings

CATEGORY_CHOICES = (
    ('processed_meat', '가공육류'),
    ('grain', '곡류'),
    ('fruit', '과일류'),
    ('snack', '과자'),
    ('oil', '기름류'),
    ('other_processed', '기타가공품'),
    ('extract', '기타추출물'),
    ('agricultural', '농산가공품'),
    ('glucose', '당류'),
    ('bean_processed', '두류가공품'),
    ('ricecake', '떡류'),
    ('noodle', '면류'),
    ('sugar_salt', '설탕소금류'),
    ('processed_marine', '수산물가공품'),
    ('seasoning', '양념'),
    ('milk', '우유'),
    ('dairy', '유제품'),
    ('meat', '육류'),
    ('drink', '음료류'),
    ('ginseng_yeast', '인삼효모류'),
    ('powder', '전분류'),
    ('pickle', '절임식품'),
    ('jelly', '젤리류'),
    ('braised', '조림류'),
    ('alcohol', '주류'),
    ('vegetable', '채소류'),
    ('chocolate', '초콜릿가공품'),
    ('spice', '향신료'),
)

INSERTION_METHOD_CHOICES = (
    ('manual', 'Manual'),
    ('photo', 'Photo'),
    ('barcode', 'Barcode'),
)


class Grocery(models.Model):
    userid = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    parsed_name = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='grain')
    qty = models.PositiveIntegerField()
    in_date = models.DateField(default=datetime.date.today)
    exp_date = models.DateField(default=datetime.date.today)
    insertion_method = models.CharField(max_length=50, choices=INSERTION_METHOD_CHOICES, default='manual')
    image = models.ImageField(upload_to="grocery", blank=True, null=True)

    def get_category_display_name(self):
        return dict(CATEGORY_CHOICES)[self.category]

    def get_insertion_method_display_name(self):
        return dict(INSERTION_METHOD_CHOICES)[self.insertion_method]
