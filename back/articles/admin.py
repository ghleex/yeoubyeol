from django.contrib import admin
from .models import Article, Comment, HonorArticle, Hashtag

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'article', 'created_at', 'updated_at',)

admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'comment',) 

admin.site.register(Comment, CommentAdmin)


class HonorArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'article', 'author', 'created_at', 'updated_at',)

admin.site.register(HonorArticle, HonorArticleAdmin)

class HashtagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'hashtag')

admin.site.register(Hashtag, HashtagAdmin)