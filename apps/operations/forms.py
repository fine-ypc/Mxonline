from apps.operations.models import UserFavorite, CourseComments
from django import forms


class UserFavForm(forms.ModelForm):  # 使用ModelForm可以使用Model的字段作为form字段
    class Meta:
        model = UserFavorite
        fields = ['fav_id', 'fav_type']  # 在此可进行字段选择


class CourseCommentsForm(forms.ModelForm):  # 使用ModelForm可以使用Model的字段作为form字段
    class Meta:
        model = CourseComments
        fields = ['course', 'comments']  # 在此可进行字段选择

