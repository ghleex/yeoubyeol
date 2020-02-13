from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.AccountList.as_view(), name='accounts'),
    path('email/', views.email_auth, name='email_auth'),
    path('social/', views.social_auth, name='social_auth'),
    path('signup/<secret_key>/', views.user_signup, name='signup'),
    path('user_detail/<int:id>/', views.user_detail, name='user_detail'),
    path('find_pwd/', views.find_pwd, name='find_pwd'),
    path('change_pwd/', views.change_pwd, name='change_pwd'),
    path('profile/', views.profile, name='profile'),
    path('check/', views.check),
    path('checknickname/', views.checknickname),
    path('logout/', views.logout),
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
