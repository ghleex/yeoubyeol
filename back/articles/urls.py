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
    path('', views.ArticleList.as_view()),
    path('<int:pk>/', views.ArticleDetail.as_view()),
    path('comment/', views.CommentList.as_view()),
    path('comment/<int:pk>/', views.CommentDetail.as_view()),
    path('search/', views.SearchResultList.as_view()),
    path('mainfeed/', views.mainfeed),
    path('follow/', views.follow),
    path('follower/', views.followerlist),
    path('following/', views.followinglist),
    path('myarticle/', views.myarticle),
    path('like/', views.like),
    path('honor/', views.honor),
    path('recommend/', views.rec_hashtag),
    path('keyword/', views.keyword),
    path('hashtag/', views.hashtag),
    path('hashtagtrend/', views.hashtagtrend),
    path('monthlytrend/', views.monthlytrend),
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
