from django.contrib import admin
from apps.users.models import UserProfile
from django.contrib.auth.admin import UserAdmin


class UserProfileAdmin(admin.ModelAdmin):  # 自定义管理器无法对新建用户的密码进行加密(所以可会换成UserAdmin)
    pass


admin.site.register(UserProfile, UserAdmin)  # 参数(要添加的model名，管理器名)
