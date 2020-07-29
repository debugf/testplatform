from django import forms
from django.core.exceptions import ValidationError

from users.models import Users


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        required=True,
        max_length=50,
        min_length=5,
        error_messages={
            "required": "该字段不能为空",
            "max_length": "最长不能超过50个字符",
            "min_length": "最小长度为5"
        })
    password = forms.CharField(
        label="密码",
        required=True,
        max_length=50,
        min_length=5,
        error_messages={
          "required": "该字段不能为空",
          "max_length": "最长不能超过50个字符",
          "min_length": "最小长度为5"
        })
    r_password = forms.CharField(
        required=True,
        max_length=50,
        min_length=5,
        label="确认密码",
        error_messages={
            "required": "该字段不能为空",
            "max_length": "最长不能超过50个字符",
            "min_length": "最小长度为5"
        })
    email = forms.CharField(
        min_length=5,
        required=True,
        label="邮箱",
        error_messages={
            "required": "该字段不能为空",
            "max_length": "最长不能超过50个字符",
            "min_length": "最小长度为5"
        }
    )

    def clean_username(self):
        val = self.cleaned_data.get('username')
        ret = Users.objects.filter(username=val)
        if not ret:
            return val
        else:
            raise ValidationError('该用户名已注册!')

    # 走完所有的校验才走clean
    def clean(self):
        pwd = self.cleaned_data.get('password')
        r_pwd = self.cleaned_data.get('r_password')
        if pwd and r_pwd:
            if pwd != r_pwd:
                raise forms.ValidationError('两次密码不一致')
        return self.cleaned_data