from rest_framework import serializers
from .models import Article, Comment, HonorArticle

class ArticleSerializer(serializers.ModelSerializer):
    class Meta(Article):
        model = Article
        fields = ('id', 'article', 'created_at', 'updated_at', 'author', 'like_users', 'hashtags', 'image')

class CommentSerializer(serializers.ModelSerializer):
    class Meta(Comment):
        model = Comment
        fields = ('id', 'article', 'author', 'comment')

class HonorArticleSerializer(serializers.ModelSerializer):
    class Meta(HonorArticle):
        model = HonorArticle
        fields = ('id', 'article', 'author', 'hashtags', 'image')