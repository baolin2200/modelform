#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2017/12/29

from django.forms import Form

# widgets 表示插件
from django.forms import widgets as widgets_bash

# fields 表示所有的字段
from django.forms import fields

from django.forms import ModelForm

from app01 import models


class LoginForm(Form):
    username = fields.CharField(
        label="用户名",
        required=True,       # 表示不能为空，默认不可为空
        error_messages={     # 错误信息 依照中文形式显示
            "required": "用户名不能为空",       # required 为真是错误信息
        },
        # 插件类型TextInput(attrs={"class": "自定义属性 多个依照空格分隔 form-control 为bootcss属性"})
        widget=widgets_bash.TextInput(attrs={"class": "form-control xxx aaa"})
    )

    password = fields.CharField(
        label="密码",
        required=True,       # 表示不能为空，默认不可为空
        error_messages={     # 错误信息 依照中文形式显示
            "required": "密码不能为空",       # required 为真是错误信息
        },
        widget=widgets_bash.PasswordInput(attrs={"class": "form-control"})
    )

    # 可以定义钩子函数
    # def clean_username(self):
    #     pass


class HostModelForm(ModelForm):
    class Meta:
        # 指定数据库的哪张表
        model = models.Host

        # 指 表中的哪个字段 "__all__" 表示所有的字段
        fields = "__all__"

        # 表示获取指 定的字段
        # fields = ["hostname", "ip"]

        # 用与 labels 调用
        labels = {
            "ip": "IP",
            "hostname": "主机名",
            "port": "端口",
            "dp": "部门",
            "user": "用户",
        }

        # 用于错误信息调用
        error_messages = {
            "ip": {"required": "IP不能为空",},
            "hostname": {"required": "用户名不能为空", },
        }

        widgets = {
            "ip": widgets_bash.TextInput(attrs={"class": "form-control"}),
            "hostname": widgets_bash.TextInput(attrs={"class": "form-control"}),
            "port": widgets_bash.TextInput(attrs={"class": "form-control xxx aaa"}),
        }

    def clean_hostname(self):
        from django.core.exceptions import ValidationError
        hostname = self.cleaned_data['hostname']

        obj = models.Host.objects.filter(hostname=hostname)
        print("clean_hostname=========", obj)
        if obj:
            raise ValidationError('主机名已存在')
        return hostname

