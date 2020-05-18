# -*- coding: utf-8 -*-
"""
将自定义Model配置到xadmin后台管理中
"""
import xadmin
from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag


class GlobalSettings(object):
    site_title = "慕学后台管理系统"  # 设置左上角系统名称
    site_footer = "慕学在线网"  # 设置底部网站出品方
    menu_style = "accordion"  # 当自定义Model注册过多时可用此收起菜单更简明


class BaseSettings(object):
    enable_themes = True  # 增加主题选择选项
    use_bootswatch = True


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']  # 看到course__name 双下划线表示访问外键指向对象的属性


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']


class CourseTagAdmin(object):
    list_display = ['course', 'tag', 'weight', 'add_time']
    search_fields = ['course', 'weight', 'tag']
    list_filter = ['course', 'tag', 'weight', 'add_time']


xadmin.site.register(Course, CourseAdmin)  # 参数(要添加的model名，管理器名)
xadmin.site.register(CourseTag, CourseTagAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)  # views下的对象可在xadmin.view.__init__下查看
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)