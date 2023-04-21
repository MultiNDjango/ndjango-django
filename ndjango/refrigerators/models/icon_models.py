from django.db import models
import json

# Create your models here.


class Location(models.Model):
    # blank allows an empty string and null means nullable in the db column
    # when user is deleted, this user field turns into None
    user = models.ForeignKey('users.CustomUser', blank=True, null=True, on_delete=models.SET_NULL)
    location = models.JSONField(null=True, blank=True)

    def __str__(self):
        tmp = json.dumps(self.location)
        info = str(self.user) + tmp
        return info

    objects = models.Manager()

    # class Meta:
    #     # db_table = 'news'
    #     managed = False  # 이걸 잠깐 추가해줍니다.


