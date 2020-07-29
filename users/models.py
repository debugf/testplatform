#users/models.py
from django.db import models

from utils.base_models import BaseModel


class Users(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='id主键')
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=50, verbose_name='密码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'lx_users'
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name