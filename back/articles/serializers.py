from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta(Article):
        model = Article
        fields = ('id', 'content', 'created_at', 'updated_at', 'like_users', 'hashtags',)
