# employees/model.py
from django.db import models


class Employees(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True)  # 主键id自增
    ename = models.CharField(verbose_name='员工姓名', max_length=32, null=False, blank=False)  # 员工姓名
    jobnumber = models.CharField(verbose_name='工号', max_length=32, null=False, blank=False, unique=True)  # 工号
    sex = models.CharField(verbose_name='性别', max_length=1, null=False, blank=False)   # 性别
    age = models.IntegerField(verbose_name='年龄', null=False, blank=False)      # 年龄
    email = models.CharField(verbose_name='邮箱', max_length=32, null=False, blank=False)  # 邮箱
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)  # 是否删除（软删除）
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)   # 修改时间

    class Meta:
        # 指定用户表名称
        db_table = 'tp_employees'
        verbose_name = '员工信息'
        verbose_name_plural = verbose_name