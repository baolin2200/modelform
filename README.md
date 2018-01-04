# modelform
使用ModelForm实现数据添加修改
==
        ModelForm这是一个神奇的组件，通过名字我们可以看出来，这个组件的功能就是把model和form组合起来；在使用Model和Form时，都需要对字段进行定义并指定类型，通过ModelForm则可以省去From中字段的定义
            
<b>ModelForm案例：GitHub地址</b>       
<a href="https://github.com/baolin2200/modelform" target="_blank" style="color: red">https://github.com/baolin2200/modelform</a>
<hr>
<b>依赖模块：</b>
```python
from django.forms import ModelForm
```
###以下为定义个别文档
#### 定义 forms.py
```python
from django.forms import Form
# widgets 表示插件 由于和 ModelForm 得 widgets 相冲突所以 as 重命名
from django.forms import widgets as widgets_bash
# fields 表示所有的字段
from django.forms import fields
# 依赖模块ModelForm
from django.forms import ModelForm
# 导入 models 表结构
from app01 import models


# 使用Form实现 用户登陆的数据清洗
class LoginForm(Form):
    username = fields.CharField(
        # 定义模板端获取得 名称 展示的汉字
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


# 使用 ModelForm 实现 主机添加 编辑的数据清洗
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

        # 定义样式
        widgets = {
            "ip": widgets_bash.TextInput(attrs={"class": "form-control"}),
            "hostname": widgets_bash.TextInput(attrs={"class": "form-control"}),
            "port": widgets_bash.TextInput(attrs={"class": "form-control xxx aaa"}),
        }

    # 定义 钩子 清洗 hostname 内容
    def clean_hostname(self):
        from django.core.exceptions import ValidationError
        hostname = self.cleaned_data['hostname']

        obj = models.Host.objects.filter(hostname=hostname)
        print("clean_hostname=========", obj)
        if obj:
            # 抛出 错误异常
            raise ValidationError('主机名已存在')
        return hostname
```

####models表结构
```python
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


# 主机表
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
```

####定义views.py文件
```python
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from app01.forms import LoginForm, HostModelForm

from app01 import models
from django.conf import settings    # 用户自定义 + 内置的 settings 配置文件
from utils.md5 import md5           # utils 为自定义工具 包
from utils.pager import Pagination  # 导入 自定义的 分页模块


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    else:
        # 将接收到的数据，传给LoginForm()类 通过form 验证；
        form = LoginForm(request.POST)
        # 通过 form 验证后，form 为True
        if form.is_valid():
            # 通过form验证的数据 存放在 cleaned_data 中
            # form.cleaned_data

            form.cleaned_data["password"] = md5(form.cleaned_data["password"])

            # 通过 **form.cleaned_data 可以将 数据依照字典形式获取 filter({"username":zhangsan,"password":1234})
            userinfo = models.UserInfo.objects.filter(**form.cleaned_data).first()  # 拿取第一个对象值

            # 如果userinfo 中有数据，即表示验证成功
            if userinfo:
                # 将 用户信息 放置到 session 中
                request.session[settings.USER_SESSION_KEY] = {"id": userinfo.pk, "username": userinfo.username}

                # 重定向 页面
                return redirect("/index/")
            else:
                # 用户验证失败
                form.add_error("password", "用户名或密码错误")

        # 存放错误信息 form.errors

        # 将 form 清洗过的 数据直接返回给 html 模板
        return render(request, "login.html", {"form": form})


def index(request):
    # return HttpResponse("验证成功！")
    return render(request, "index.html")


def testt(request):
    user = models.UserInfo.objects.filter(username="baolin")
    print(user.username)
    return HttpResponse("OK")


def host(request):
    # 统计出一共有多少条 数据
    all_count = models.Host.objects.all().count()
    # page_obj = Pagination 方法需要 3个 参数(请求当前页码，总数据条数，该应用路径)
    # page_obj = Pagination(request.GET.get('page'),all_count,'/host/')
    page_obj = Pagination(request.GET.get('page'),all_count,request.path_info)

    # host_list = models.Host.objects.all()[本页内容的开始,本页内容的结束]
    host_list = models.Host.objects.all()[page_obj.start:page_obj.end]

    # render(request, 页面, {展示内容，展示的 html页码})
    return render(request, 'host.html', {'host_list': host_list, 'page_html': page_obj.page_html()})


def add_host(request):
    if request.method == "GET":
        form = HostModelForm()
        return render(request, "add_host.html", {"form": form})

    else:
        # 将模板传入的数据 交给 HostModelForm() 清洗
        form = HostModelForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            # form.save() 将通过 ModelForm 清洗的 数据直接保存到数据库中
            obj = form.save()
            return redirect("/host/")
        return render(request, "add_host.html", {"form": form})


def edit_host(request, nid):
    obj = models.Host.objects.filter(id=nid).first()

    if not obj:
        return HttpResponse("数据不存在！")

    if request.method == "GET":
        # 将 要修改的数据对象，传给 HostModelForm() 进行清洗
        form = HostModelForm(instance=obj)

        return render(request, "edit_host.html", {"form": form})

    else:
        # 如果是 post 提交，将数据传给 HostModelForm() 清洗，并指定是 instance 的对象值
        form = HostModelForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/host/")
        return render(request, "edit_host.html", {"form": form})
```
