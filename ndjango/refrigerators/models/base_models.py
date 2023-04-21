import datetime
from django.db import models

CATEGORY_CHOICES = (
    ('grain', '곡물'),
    ('nut', '견과류'),
    ('fruit', '과일'),
    ('vegetable', '채소'),
    ('meat', '육류'),
    ('dairy', '유제품'),
    ('marine', '수산물'),
    ('seasoning', '조미료'),
    ('spice', '향신료'),
    ('processed', '가공식품'),
)

# Create your models here.
class Grocery(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='grain')
    qty = models.PositiveIntegerField()
    in_date = models.DateField(default=datetime.date.today)
    exp_date = models.DateField(default=datetime.date.today)
    image = models.ImageField(upload_to="grocery", blank=True, null=True)

    def get_category_display_name(self):
        return dict(CATEGORY_CHOICES)[self.category]

    # class Meta:
    #     managed = False