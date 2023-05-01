from django.db import models

# Create your models here.


class BarcodeInfo(models.Model):
    bar_id = models.IntegerField(null=False)
    barcode = models.CharField(max_length=500, null=False, primary_key=True)
    pd_name = models.CharField(max_length=500, null=False)
    category = models.CharField(max_length=500, null=False)
    re_category = models.CharField(max_length=500, null=False, default='')
    best_before = models.IntegerField()
    supplier = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Icon(models.Model):
    icon_id = models.IntegerField(null=False, primary_key=True)
    re_category = models.CharField(max_length=500, null=False, default='')
    icon_img = models.BinaryField(blank=True)


