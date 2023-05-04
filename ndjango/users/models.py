from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# import jsonfield

from .managers import CustomUserManager


DIET_CHOICES = (
    (-1, '다이어트'),
    (0, '유지'),
    (1, '증량')
)



# AbstractBaseUser를 사용하면 로그인 방식도 변경, 원하는 필드들로 유저 모델을 구성
# PermissionsMixin 을 함께 상속하면 Django의 기본그룹, 허가권 관리 등을 사용
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    nickname = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    diet = models.SmallIntegerField(choices=DIET_CHOICES, null=True, blank=True)
    allergy = models.JSONField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email" # 로그인 ID로 사용할 필드
    REQUIRED_FIELDS = ['nickname'] # 필수 작성 필드

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_nickname(self):
        return self.nickname

