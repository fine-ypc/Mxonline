from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.courses.models import Course, CourseTag, CourseResource, Video
from apps.operations.models import UserCourse
from apps.operations.models import UserFavorite, CourseComments
from pure_pagination import PageNotAnInteger, Paginator


class CourseVideoView(LoginRequiredMixin, View):
    """
    获取课程章节评论页
    """
    login_url = '/login/'  # 访问视图前登录

    def get(self, request, course_id, video_id, *args, **kwargs):

        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1  # 点击数加一
        course.save()

        # 获取 课程评论
        course_comments = CourseComments.objects.filter(course=course).order_by("-add_time")


        # 获取当前Video
        video = Video.objects.filter(id=int(video_id))

        #  学习过该课程的学生，还学过哪些课程
        user_courses = UserCourse.objects.filter(course=course)  # 获取所有与当前课程绑定的 用户课程
        user_ids = [user_course.user.id for user_course in user_courses]  # 获取所有用户id
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]  # 获取所有用户学习的课程 (倒序前5)
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]  #  过滤不显示当前课程

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-play.html', {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "course_comments": course_comments,
            "video": video
        })


class CourseCommentsView(LoginRequiredMixin, View):
    """
    获取课程章节评论页
    """
    login_url = '/login/'  # 访问视图前登录

    def get(self, request, course_id, *args, **kwargs):

        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1  # 点击数加一
        course.save()

        # 获取 课程评论
        course_comments = CourseComments.objects.filter(course=course).order_by("-add_time")

        # 查询课程和用户是否关联  (点击开始学习课程后  需生成 课程和用户联系的记录)
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1  # 用户和课程关联后  课程的学生数加一
            course.save()

        #  学习过该课程的学生，还学过哪些课程
        user_courses = UserCourse.objects.filter(course=course)  # 获取所有与当前课程绑定的 用户课程
        user_ids = [user_course.user.id for user_course in user_courses]  # 获取所有用户id
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]  # 获取所有用户学习的课程 (倒序前5)
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]  #  过滤不显示当前课程

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-comment.html', {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "course_comments": course_comments
        })


class CourseLessonView(LoginRequiredMixin, View):
    """
    获取课程章节信息页
    """
    login_url = '/login/'  # 访问视图前登录

    def get(self, request, course_id, *args, **kwargs):

        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1  # 点击数加一
        course.save()

        # 查询课程和用户是否关联  (点击开始学习课程后  需生成 课程和用户联系的记录)
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1  # 用户和课程关联后  课程的学生数加一
            course.save()

        #  学习过该课程的学生，还学过哪些课程
        user_courses = UserCourse.objects.filter(course=course)  # 获取所有与当前课程绑定的 用户课程
        user_ids = [user_course.user.id for user_course in user_courses]  # 获取所有用户id
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]  # 获取所有用户学习的课程 (倒序前5)
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]  #  过滤不显示当前课程

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-lesson.html', {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses
        })


class CourseDetailView(View):
    """获取课程详情页"""
    def get(self, request, course_id, *args, **kwargs):

        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1  # 点击数加一
        course.save()

        # 获取课程收藏的状态
        has_course_fav = False

        # 获取机构收藏的状态
        has_org_fav = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):  # 课程为1
                has_course_fav = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):  # 机构为2
                has_org_fav = True

        #  筛选tag相同的推荐课程
        tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in tags]
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id).order_by('-weight')

        related_courses = []  # 使用集合避免出现重复(因为课程间可能有多个tag相同)
        for course_tag in course_tags:
            if course_tag not in related_courses:
                related_courses.append(course_tag.course)

        return render(request, 'course-detail.html', {
            "course": course,
            "has_course_fav": has_course_fav,
            "has_org_fav": has_org_fav,
            "related_courses": related_courses
        })


class CourseListView(View):
    """获取课程列表"""
    def get(self, request, *args, **kwargs):
        all_courses = Course.objects.order_by("-add_time")
        hot_courses = Course.objects.order_by("-click_nums")

        # 分页
        try:
            page = request.GET.get('page', 1)  # 从请求中获取页码(默认为1)
        except PageNotAnInteger:
            page = 1

        sort = request.GET.get("sort", "")
        if sort == "students":
            all_courses = Course.objects.order_by("-students")

        elif sort == "hot":
            all_courses = Course.objects.order_by("-click_nums")

        # 前端分页配置
        p = Paginator(all_courses, per_page=3, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses
        })
