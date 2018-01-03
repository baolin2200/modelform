from django.db import models

# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    def __str__(self):
        return self.username


# 部门表
class Departement(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Host(models.Model):

    # blank=True 表示可以为空
    hostname = models.CharField(max_length=32)

    # GenericIPAddressField 与 model form 一起使用才有效果，否则和 CharField效果一样
    # ip = models.GenericIPAddressField(protocol="ipv4")

    ip = models.CharField(max_length=32)
    port = models.IntegerField()

    # 一对多 1个用户多个 主机
    user = models.ForeignKey(to="UserInfo", default=1)

    # 多对多 主机表 和 部门表
    dp = models.ManyToManyField(to="Departement")

