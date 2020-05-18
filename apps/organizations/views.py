from django.shortcuts import render
from django.views.generic.base import View
from apps.organizations.models import CourseOrg, City
from django.http import JsonResponse
from apps.organizations.forms import AddAskForm
from apps.operations.models import UserFavorite
from pure_pagination import PageNotAnInteger, Paginator


class OrgDescView(View):
    def get(self, request, org_id,  *args, **kwargs):
        """机构介绍页面"""
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 此处为前端提供 收藏按钮 的是否收藏状态  {前端默认显示收藏，点击收藏后有相应但刷新后消失}
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html',
                      {
                          "org_desc": current_page,
                          "course_org": course_org,
                          "current_page": current_page,
                          "has_fav": has_fav
                      })


class OrgCourseView(View):
    def get(self, request, org_id,  *args, **kwargs):
        """机构课程页面"""
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_course = course_org.course_set.all()
        try:
            page = request.GET.get('page', 1)  # 从请求中获取页码(默认为1)
        except PageNotAnInteger:
            page = 1

        # 前端分页配置
        p = Paginator(all_course, per_page=4, request=request)
        courses = p.page(page)

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html',
                      {
                          "all_courses": courses,
                          "course_org": course_org,
                          "current_page": current_page,
                          "has_fav": has_fav
                      })


class OrgTeacherView(View):
    def get(self, request, org_id,  *args, **kwargs):
        """机构讲师页面"""
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_teacher = course_org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html',
                      {
                          "all_teacher": all_teacher,
                          "course_org": course_org,
                          "current_page": current_page,
                          "has_fav": has_fav
                      })


class OrgHomeView(View):
    def get(self, request, org_id,  *args, **kwargs):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_courses = course_org.course_set.all()[:3]  # 获取外键所有对象时的快捷方法 *_set
        all_teacher = course_org.teacher_set.all()[:1]

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html',
                      {
                          "all_courses": all_courses,
                          "all_teacher": all_teacher,
                          "course_org": course_org,
                          "current_page": current_page,
                          "has_fav": has_fav
                      })


class UserAskView(View):
    def post(self, request, *args, **kwargs):
        user_ask = AddAskForm(request.POST)
        if user_ask.is_valid():
            user_ask.save(commit=True)  # 因form继承了Modelform，所以可以直接提交数据库(commit为True时)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错"
            })


class OrgListView(View):
    def get(self, request, *args, **kwargs):  # django自动注入request请求
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        try:
            page = request.GET.get('page', 1)  # 从请求中获取页码(默认为1)
        except PageNotAnInteger:
            page = 1

        # 筛选课程机构(通过机构类别)
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 筛选课程机构(通过城市类别)
        city_id = request.GET.get("city", "")
        if city_id:
            if city_id.isdigit():  # 此函数判断字符串内是否是数字 例如 '2'(原因:通过url直接访问的话可能是字符串，导致出错)
                all_orgs = all_orgs.filter(city_id=int(city_id))

        # 根据学习人数和课程数排序
        sort = request.GET.get("sort", "")
        if sort == 'student':
            all_orgs = all_orgs.order_by('-students')  # 加负号表示倒序
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()

        # 前端分页配置
        p = Paginator(all_orgs, per_page=4, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            'all_orgs': orgs,
            'org_nums': org_nums,
            'all_citys': all_citys,
            'category': category,
            'city_id': city_id,
            'sort': sort,
            'hot_orgs': hot_orgs
        })
