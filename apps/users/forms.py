from django import forms
from captcha.fields import CaptchaField
from apps.users.models import UserProfile
import redis
from MxOnline.settings import REDIS_HOST, REDIS_PORT


class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True, min_length=3)

    def clean_mobile(self):
        mobile = self.data.get("mobile")
        user = UserProfile.objects.filter(mobile=mobile)
        if user:
            raise forms.ValidationError("该手机号码已注册")
        return mobile

    def clean_code(self):  # 在验证表单前(is_valid)先验证此项(code属性) 此方法自启动不需要调用
        mobile = self.data.get("mobile")
        code = self.data.get("code")  # 此处从data中取值较为稳妥(更早的数值集)，cleaned_data(较晚生成的数值集)中此时不一定存在

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf-8', decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return code


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicCodeLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):  # 在验证表单前(is_valid)先验证此项(code属性) 此方法自启动不需要调用
        mobile = self.data.get("mobile")
        code = self.data.get("code")  # 此处从data中取值较为稳妥(更早的数值集)，cleaned_data(较晚生成的数值集)中此时不一定存在

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf-8', decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data
