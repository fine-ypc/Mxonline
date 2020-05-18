from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = "用户"  # 将后台管理系统中显示的model名变为中文
