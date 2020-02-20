from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Waiting, Notification, AccountCookie

User = get_user_model()

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'username', 'password', 'pic_name',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'nickname', 'intro', 'pic_name', 'username', 'followers', 'followings', 'social',)


class WaitingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiting
        fields = ('username', 'secret_key', 'created_at',)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'nickname', 'is_read', 'created_at', 'message', 'send_user', 'article_no',)
        
class AccountCookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountCookie
        fields = ('username', 'login_at', 'token_1', 'token_2',)