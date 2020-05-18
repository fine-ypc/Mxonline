from django.shortcuts import render
from django.views.generic.base import View  # django提供的View中提供了dispatch方法 分发请求到get或post函数
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse  # url重定向
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicCodeLoginForm, RegisterGetForm, RegisterPostForm
from apps.util.YunPian import send_single_sms
from apps.util.random_str import generate_random
from MxOnline.settings import yunpian_apikey, REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile
import redis


class RegisterView(View):
    def get(self, request, *args, **kwargs):  # django自动注入request请求
        r_form = RegisterGetForm()
        return render(request, "register.html", {
            "register_get_form": r_form
        })

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "register.html", {
                "register_get_form": register_get_form,  # 为了在前端页面显示图形验证码
                "register_post_form": register_post_form  # 为了在前端页面显示错误信息，所以传此form
            })


class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):  # django自动注入request请求
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        login_form = DynamicLoginForm()
        next_point = request.GET.get("next", "")
        return render(request, "login.html", {
            "login_form": login_form,
            "next_point": next_point
        })

    def post(self, request, *args, **kwargs):
        login_form = DynamicCodeLoginForm(request.POST)
        dynamic_login = True
        if login_form.is_valid():
            mobile = login_form.cleaned_data["mobile"]
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                # 若未查询到用户则创建新用户，密码使用随机生成并加密
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            next_point = request.GET.get("next", "")
            if next_point:
                return HttpResponseRedirect(next_point)
            return HttpResponseRedirect(reverse('index'))
        else:
            d_form = DynamicLoginForm()  # 当前视图返回的页面参数中没有captcha,会导致图片验证码无法加载所以需要复用一下这个表单
        return render(request, "login.html", {"dynamic_login_form": login_form,
                                              "dynamic_captcha_form": d_form,
                                              "dynamic_login": dynamic_login})


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        res_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            # 随机生成数字验证码(短信注册用)
            code = generate_random(4, 0)
            res_json = send_single_sms(yunpian_apikey, code, mobile=mobile)
            if res_json["code"] == 0:
                res_dict["status"] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf-8', decode_responses=True)
                r.set(str(mobile), code)  # 设置键值对的值
                r.expire(str(mobile), 60*5)  # 设置过期时间 单位(s)
            else:
                res_dict["msg"] = res_json["meg"]
        else:
            for key, value in send_sms_form.errors.items():
                res_dict[key] = value[0]
        return JsonResponse(res_dict)


class LogoutView(View):
    def get(self, request, *args, **kwargs):  # django自动注入request请求
        logout(request)
        next_point = request.GET.get("next", "")
        if next_point:
            return HttpResponseRedirect(next_point)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request, *args, **kwargs):  # django自动注入request请求
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        login_form = DynamicLoginForm()
        next_point = request.GET.get("next", "")
        return render(request, "login.html", {
            "login_form": login_form,
            "next_point": next_point
        })

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            # 此处也可以导入UserProfile,带入账户名和密码进行数据库查询，
            # 但需要明确加密和解密库，当前不知道如何解django自带加密机制
            if user is not None:
                login(request, user)  # 登陆(内部保存用户id至session(加密的cookie))
                next_point = request.GET.get("next", "")
                if next_point:
                    return HttpResponseRedirect(next_point)
                return HttpResponseRedirect(reverse("index"))  # 重定向回index界面
            else:
                # 若未查询到用户
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            # 若未查询到用户
            return render(request, "login.html", {"login_form": login_form})


