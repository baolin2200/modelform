#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2017/12/29
from django.conf import settings
from django.shortcuts import redirect


# 该 MiddlewareMixin 类为默认继承类，在Django 1.10 之后需要该类的继承，1.7-1.8 无需该类继承
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class M1(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):

        # path_info 获取当前URL 的路径值，不带参数的路径
        # 如果Url 为 login 就返回一个None 让请求继续
        if request.path_info == "/login/":
            return None
        else:
            user_info = request.session.get(settings.USER_SESSION_KEY)
            if not user_info:
                return redirect("/login/")

    def process_response(self, request, response):
        print("m1.process_response")
        return response


