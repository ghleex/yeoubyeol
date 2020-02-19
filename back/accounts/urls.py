from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.AccountList.as_view()),
    path('<int:pk>/', views.AccountDetail.as_view()),
    path('email/', views.email_auth),
    path('google/', views.google),
    path('signup/<secret_key>/', views.user_signup),
    path('checkpwd/', views.checkpwd),
    path('findpwd/', views.findpwd),
    path('changepwd/', views.changepwd),
    path('profile/', views.profile),
    path('checknickname/', views.checknickname),
    path('check/', views.check_is_logged_in),
    path('logout/', views.logout),
    path('noti/<int:pk>/', views.NotificationList.as_view()),
    path('noti_is_read/<int:pk>/', views.NotificationIsLeftList.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 