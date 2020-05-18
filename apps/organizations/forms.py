from apps.operations.models import UserAsk
from django import forms


class AddAskForm(forms.ModelForm):  # 使用ModelForm可以使用Model的字段作为form字段
    mobile = forms.CharField(min_length=11, max_length=11, required=True)  # 对model转化的字段进行重写

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']  # 在此可进行字段选择
