from django.db import models

from utils.base_models import BaseModel


class Projects(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='id主键')
    name = models.CharField(max_length=50, unique=True, verbose_name='项目名')
    leader = models.CharField(max_length=50, unique=True, verbose_name='负责人')
    tester = models.CharField(max_length=50, verbose_name='测试人员')
    programer = models.CharField(max_length=50, verbose_name='开发人员')
    publish_app = models.CharField(max_length=50, verbose_name='应用名称')
    desc = models.CharField(max_length=200, verbose_name='简要描述', blank=True, default="", null=True)

    class Meta:
        db_table = 'lx_projects'
        verbose_name = '项目信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name