# user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser  # AbstractUser 장고에서 사용하는 기본 유저 모델
from django.conf import settings


# Create your models here.
class UserModel(AbstractUser):
    class Meta:  # 데이터 베이스 정보를 넣어 주는 역할
        db_table = "my_user"  # 테이블 이름

    bio = models.CharField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
