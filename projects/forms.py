# projects/forms.py
from django import forms
from django.core.exceptions import ValidationError

from projects.models import Projects


class CreateForm(forms.Form):
    name = forms.CharField(
        label="项目名",
        required=True,
        max_length=50,
        min_length=2,
        error_messages={
            "required": "项目名不能为空",
            "max_length": "项目名最长不能超过50个字符",
            "min_length": "项目名最小长度为2"
        })
    leader = forms.CharField(
        label="负责人",
        required=True,
        max_length=50,
        min_length=2,
        error_messages={
            "required": "负责人不能为空",
            "max_length": "负责人最长不能超过50个字符",
            "min_length": "负责人最小长度为2"
        })
    tester = forms.CharField(
        label="测试人员",
        required=True,
        max_length=50,
        min_length=2,
        error_messages={
            "required": "测试人员不能为空",
            "max_length": "测试人员最长不能超过50个字符",
            "min_length": "测试人员最小长度为2"
        })
    programer = forms.CharField(
        label="开发人员",
        required=True,
        max_length=50,
        min_length=2,
        error_messages={
            "required": "开发人员不能为空",
            "max_length": "开发人员最长不能超过50个字符",
            "min_length": "开发人员最小长度为2"
        })
    publish_app = forms.CharField(
        label="应用名称",
        required=True,
        max_length=50,
        min_length=2,
        error_messages={
            "required": "应用名称不能为空",
            "max_length": "应用名称最长不能超过50个字符",
            "min_length": "应用名称最小长度为2"
        })
    desc = forms.CharField(
        label="简要描述",
        required=False,
        max_length=200,
        error_messages={
            "max_length": "简要描述最长不能超过200个字符",
        })

    def clean_name(self):
        val = self.cleaned_data.get("name")
        ret = Projects.objects.filter(name=val).values("name")
        if not ret:
            return val
        else:
            raise ValidationError("该项目名已存在!")


class UpdateForm(forms.Form):
    name = forms.CharField(
        label="项目名",
        required=False,
        max_length=50,
        min_length=2,
        error_messages={
            "max_length": "项目名最长不能超过50个字符",
            "min_length": "项目名最小长度为2"
        })
    leader = forms.CharField(
        label="负责人",
        required=False,
        max_length=50,
        min_length=2,
        error_messages={
            "max_length": "负责人最长不能超过50个字符",
            "min_length": "负责人最小长度为2"
        })
    tester = forms.CharField(
        label="测试人员",
        required=False,
        max_length=50,
        min_length=2,
        error_messages={
            "max_length": "测试人员最长不能超过50个字符",
            "min_length": "测试人员最小长度为2"
        })
    programer = forms.CharField(
        label="开发人员",
        required=False,
        max_length=50,
        min_length=2,
        error_messages={
            "max_length": "开发人员最长不能超过50个字符",
            "min_length": "开发人员最小长度为2"
        })
    publish_app = forms.CharField(
        label="应用名称",
        required=False,
        max_length=50,
        min_length=2,
        error_messages={
            "max_length": "应用名称最长不能超过50个字符",
            "min_length": "应用名称最小长度为2"
        })
    desc = forms.CharField(
        label="简要描述",
        required=False,
        max_length=200,
        error_messages={
            "max_length": "简要描述最长不能超过200个字符",
        })
