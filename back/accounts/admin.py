from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Notification, Waiting

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # fieldsets : 관리자 리스트 화면에서 출력될 폼 설정 부분
    UserAdmin.fieldsets[1][1]['fields'] += ('nickname', 'intro', 'followers', 'pic_name',)
    # add_fieldsets : User 객체 추가 화면에 출력될 입력 폼 설정 부분
    UserAdmin.add_fieldsets += (
        (('Additional Info'),{'fields':('nickname', 'intro', 'followers', 'pic_name')}),
    )
    list_display = ('username', 'nickname', 'email', 'intro', 'pic_name', 'is_staff',)

admin.site.register(User, CustomUserAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'is_read', 'created_at', 'message', 'send_user',)

admin.site.register(Notification, NotificationAdmin)


class WaitingAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'secret_key', 'created_at',)

admin.site.register(Waiting, WaitingAdmin)
