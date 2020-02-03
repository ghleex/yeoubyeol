from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Waiting

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