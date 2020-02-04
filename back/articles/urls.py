from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from . import views

app_name = 'articles'
urlpatterns = [
   #  path('articles/', views.article_list),
    path('', views.ArticleList.as_view(), name='articles'),
    path('<int:pk>/', views.ArticleDetail.as_view(), name='detail'),
    path('search/', views.SearchResultList.as_view(), name='search'),
    path('follower/', views.FollowerList.as_view(), name='follower'),
    path('following/', views.FollowingList.as_view(), name='following'),
]
