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
    path('google/', views.google, name='google'),
    path('signup/<secret_key>/', views.user_signup, name='signup'),
    path('user_detail/<int:id>/', views.user_detail, name='user_detail'),
    path('checkpwd/', views.checkpwd),
    path('findpwd/', views.findpwd, name='findpwd'),
    path('changepwd/', views.changepwd, name='changepwd'),
    path('profile/', views.profile, name='profile'),
    path('checknickname/', views.checknickname),
    path('check/', views.check),
    path('logout/', views.logout),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 