# -*- coding: utf-8 -*-
"""
将自定义Model配置到xadmin后台管理中
"""
import xadmin
from apps.organizations.models import Teacher, City, CourseOrg


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']


class CityAdmin(object):
    list_display = ["id", "name", "desc"]  # 配置显示的字段类型
    search_fields = ["name", "desc"]  # 显示搜索框并定义可以搜索的参数类型
    list_filter = ["name", "desc", "add_time"]  # 定义可用来过滤的参数类型
    list_editable = ["name", "desc"]  # 设置可直接修改的参数类型(不用点进去详情)


xadmin.site.register(Teacher, TeacherAdmin)  # 参数(要添加的model名，管理器名)
xadmin.site.register(CourseOrg, CourseOrgAdmin)  # 参数(要添加的model名，管理器名)
xadmin.site.register(City, CityAdmin)  # 参数(要添加的model名，管理器名)
