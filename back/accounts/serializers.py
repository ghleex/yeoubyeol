from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Waiting, Notification

User = get_user_model()

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'username', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'nickname', 'intro', 'username', 'followers', 'followings')


class WaitingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiting
        fields = ('username', 'secret_key', 'created_at')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('username', 'is_read', 'created_at', 'message', 'send_user')
        