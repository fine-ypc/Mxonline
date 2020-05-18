from django.shortcuts import render
from apps.operations.forms import UserFavForm, CourseCommentsForm
from apps.operations.models import UserFavorite, CourseComments
from apps.courses.models import Course, CourseOrg, Teacher
from django.http import JsonResponse
from django.views.generic.base import View


class CourseCommentsView(View):
    def post(self, request, *args, **kwargs):
        """
        收录课程评论
        """
        #  用户未登录
        if not request.user.is_authenticated:
            return JsonResponse({  # 返回值给js
                "status": "fail",
                "msg": "用户未登录"
            })

        # 获取 课程评论 对象
        course_comments_form = CourseCommentsForm(request.POST)

        if course_comments_form.is_valid():
            course = course_comments_form.cleaned_data["course"]
            comments = course_comments_form.cleaned_data["comments"]

            course_comment = CourseComments()
            course_comment.user = request.user
            course_comment.course = course
            course_comment.comments = comments
            course_comment.save()

            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


class UserFavView(View):
    def post(self, request, *args, **kwargs):
        """
        用户收藏，取消收藏
        """
        #  用户未登录
        if not request.user.is_authenticated:
            return JsonResponse({  # 返回值给js
                "status": "fail",
                "msg": "用户未登录"
            })
        user_fav_form = UserFavForm(request.POST)

        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]

            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)

            if existed_records:
                existed_records.delete()

                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1  # 收藏数减一
                    course.save()

                if fav_type == 2:
                    course = CourseOrg.objects.get(id=fav_id)
                    course.fav_nums -= 1  # 收藏数减一
                    course.save()

                if fav_type == 3:
                    course = Teacher.objects.get(id=fav_id)
                    course.fav_nums -= 1  # 收藏数减一
                    course.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })

            else:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏"
                })
        else:
            return JsonResponse({
            "status": "fail",
            "msg": "参数错误"
        })


