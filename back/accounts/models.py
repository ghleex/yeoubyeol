from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from articles.models import Comment
import secrets


# Create your models here.
class User(AbstractUser):
    username = models.EmailField(blank=False, unique=True)
    intro = models.CharField(max_length=50, default="ㄴr는 ㄱr끔 눈물을 흘린ㄷr....★")
    nickname = models.CharField(max_length=20, blank=False, unique=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True)

REQUIRED_FIELDS = ['nickname', ]


class Waiting(models.Model):
    username = models.EmailField(blank=False)
    secret_key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class pwd_find(models.Model):
    username = models.EmailField(blank=False)
    secret_key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=False)


# 알림센터 모델링
class Notification(models.Model):
    # noti_id: 알림 종류(팔로우 요청, 댓글 등)
    noti_id = models.IntegerField()
    # is_read: 열람 여부
    is_read = models.BooleanField(default=0)
    # created_at: noti 생성 시각
    created_at = models.DateTimeField(auto_now_add=True)
    # message: noti 내용
    message = models.TextField()
    # user: 현재 사용자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
