from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)  # 主键id自增
    username = models.CharField(max_length=32, null=False, blank=False, unique=True)  # 用户名
    password = models.CharField(max_length=32, null=False, blank=False)  # 密码
    email = models.CharField(max_length=32, null=False, blank=False, unique=True)  # 邮箱
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        # 指定用户表名称
        db_table = 'tp_users'