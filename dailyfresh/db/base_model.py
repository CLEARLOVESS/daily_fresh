from django.db import models


class BaseModel(models.Model):
    """自定义抽象模型类，项目应用的模型类统一继承此类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        # 说明此类是一个抽象基类
        abstract = True
