from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'articles'
urlpatterns = [
   #  path('articles/', views.article_list),
    path('', views.ArticleList.as_view(), name='articles'),
    path('mainfeed/', views.mainfeed),
    path('<int:pk>/', views.ArticleDetail.as_view(), name='detail'),
    path('search/', views.SearchResultList.as_view(), name='search'),
    path('update/', views.update),
    path('follower/', views.FollowerList.as_view(), name='follower'),
    path('followerlist/', views.followerlist, name='follower_list'),
    path('following/', views.followinglist, name='following'),
    path('myarticle/', views.myarticle),
    path('like/', views.like, name='like'),
    path('comment/', views.CommentList.as_view(), name='comment'),
    path('comment/<int:pk>', views.CommentList.as_view(), name='comment'),
    path('honor/', views.honor, name='honor'),
    path('recommend/', views.recommend),
    path('hashtag/', views.hashtag),
    path('keyword/', views.keyword),
    path('hashtagtrend/', views.trend),
    path('monthlytrend/', views.monthlytrend),
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
