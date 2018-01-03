from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from app01.forms import LoginForm, HostModelForm

from app01 import models
from django.conf import settings    # 用户自定义 + 内置的 settings 配置文件
from utils.md5 import md5           # utils 为自定义工具 包
from utils.pager import Pagination  # 导入 分页显示


# 装饰器实现用户认证
# def auth(func):
#     def inner(request, *args, **kwargs):
#         # ####可以写装饰内容
#         # 验证 session 中是否记录了 USER_SESSION_KEY 数据，如果没有 跳转到 /login/ 去
#         user_info = request.session.get(settings.USER_SESSION_KEY)
#         if not user_info:
#             return redirect("/login/")
#         # ########
#         # 执行试图函数
#         response = func(request, *args, **kwargs)
#         return response
#     return inner


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

            # 通过自定义 md5 模块验证密码
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


def Create_data(request):
    # 插入数据速度快消耗资源少
    Hostlist=[]
    for i in range(303):
        # 生成book对象
        host_obj = models.Host(hostname="c"+str(i)+".com", ip="1.1.1.1", port="80")
        Hostlist.append(host_obj)

    # bulk_create 将实例化的 列表 插入到数据库中
    models.Host.objects.bulk_create(Hostlist)
    return HttpResponse("OK")

# mark_safe用于标记 html 语句，将html安装原有的样式显示


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









