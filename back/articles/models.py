from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail, ResizeToFit

# Create your models here.
class Hashtag(models.Model):
    hashtag = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.hashtag


class Article(models.Model):
    article = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles', blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    image = ProcessedImageField(
        processors=[ResizeToFit(300, 300)],
        format='JPEG',
        options={'quality': 90},
        upload_to='articles/images',
        blank=True,
    )

    class Meta:
        ordering = ('-pk',)
    
    def __str__(self):
        return self.article


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('pk',)
    
    def __str__(self):
        return self.comment


class HonorArticle(models.Model):
    article = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    image = ProcessedImageField(
        processors=[Thumbnail(300, 300)],
        format='JPEG',
        options={'quality': 90},
        upload_to='articles/images',
        blank=True,
    )

    class Meta:
        ordering = ('-pk',)
    
    def __str__(self):
        return self.h_article
