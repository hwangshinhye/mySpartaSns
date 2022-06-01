# tweet/models.py
from django.db import models
from user.models import UserModel
from taggit.managers import TaggableManager


# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # ForeignKey: 다른 데이터베이스에서 내용(모델)을 가져오겠다
    content = models.CharField(max_length=256)
    tags = TaggableManager(blank=True) # blank=True: 비어 있어도 작동 하겠다
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TweetComment(models.Model):
    class Meta:
        db_table = "comment"

    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
