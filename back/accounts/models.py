from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from articles.models import Comment
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFit
import secrets


# Create your models here.
class User(AbstractUser):
    username = models.EmailField(blank=False, unique=True)
    intro = models.CharField(max_length=50, default="ㄴr는 ㄱr끔 눈물을 흘린ㄷr....★")
    nickname = models.CharField(max_length=20, blank=False, unique=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True)
    social = models.BooleanField(default=False)
    pic_name = ProcessedImageField(
        processors=[ResizeToFit(300, 300)],
        format='JPEG',
        options={'quality': 90},
        upload_to='accounts/pic_names',
        blank=True,
    )

REQUIRED_FIELDS = ['nickname', ]


class Waiting(models.Model):
    username = models.EmailField(blank=False)
    secret_key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class PwdFind(models.Model):
    username = models.EmailField(blank=False)
    secret_key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=False)


# 알림센터 모델링
class Notification(models.Model):
    # username: 알림 받는 사람
    nickname = models.IntegerField()
    # is_read: 열람 여부
    is_read = models.BooleanField(default=0)
    # created_at: noti 생성 시각
    created_at = models.DateTimeField(auto_now_add=True)
    # message: noti 내용
    message = models.CharField(max_length=100)
    # send_user: 알림 보내는 사람
    send_user = models.IntegerField()
    # article_no: 해당 글 번호
    article_no = models.IntegerField(null=True)
    
    class Meta:
        ordering = ('-pk',)


class AccountCookie(models.Model):
    username = models.EmailField(blank=False, unique=True)
    login_at = models.DateTimeField(auto_now=True)  
    token_1 = models.TextField()
    token_2 = models.TextField(blank=True)
