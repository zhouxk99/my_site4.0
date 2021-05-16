import datetime
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
import pymysql
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import F
from django.http import JsonResponse

# （from Macbook）Create your views hereeeeeee.
# (from Thinkpad)Hello!!!
from app01 import models


def toast(request):
    messages.success(request, "哈哈哈哈")


def test_view(request):
    print("执行业务逻辑计算中")

    return HttpResponse("test_view success")


def runoob(request):
    # context          = {}
    # context['hello'] = 'Hello World!'
    # return render(request, 'runoob.html', context)

    views_name = "菜鸟教程"
    return render(request, "runoob.html", {"name": views_name})


@csrf_exempt
def login(request):
    error_msg = ''
    if request.method == "POST":
        user = request.POST.get('user', None)  # 避免提交空，时异常
        # user = user.strip()  # 用户输入末尾有空格是去空格
        pwd = request.POST.get('pwd', None)
        obj = models.Account.objects.filter(username=user, password=pwd).first()
        # obj = models.Account.objects.get(name=user)

        # obj = models.Account.username.filter(username=user)

        # if user == "root" and pwd == "123":
        if obj:
            print('user=' + user, 'pwd=' + pwd)
            res = redirect("/index/")
            res.set_cookie('login_user', user)
            return res
        else:
            error_msg = "账号或者密码不对"
            print(error_msg)
            print('user=', user, 'pwd=', pwd)
    return render(request, 'login.html', {'error_msg': error_msg})


###################################################
@csrf_exempt
def register(request):
    error_msg = ''
    success_msg = ''
    if request.method == "POST":
        user = request.POST.get('user', None)  # 避免提交空，时异常
        # user = user.strip()  # 用户输入末尾有空格是去空格
        pwd = request.POST.get('pwd', None)
        pwd_again = request.POST.get('pwd_again', None)
        email = request.POST.get('email', None)
        obj = models.Account.objects.filter(username=user).first()

        if obj:
            print('XXuser=' + user, 'pwd=' + pwd)
            res = redirect("/login/")
            error_msg = '账户已存在！'
            messages.error(request, '账户已存在!')
            # return redirect('../register', {'error_msg': error_msg})
        elif pwd != pwd_again:
            messages.error(request, '两次密码不一致!')
        else:
            models.Account.objects.create(username=user, password=pwd, email=email)
            print('add account success!')
            print('user=', user, 'pwd=', pwd, 'email=', email)
            success_msg = '注册成功！'
            return redirect('/index/', {'success_msg': success_msg})
    return render(request, 'register.html', {'error_msg': error_msg, 'success_msg': success_msg})


##########################################

def base(request):
    return render(request, 'base.html')


def index(request):
    # login_user = request.COOKIES.get('login_user')
    # if not login_user:
    #     return redirect('../login')
    # print(request.GET.items)
    # print(models)

    article_list = models.Article.objects.all()
    order_10_list = models.Article.objects.order_by('-create_date')[:10]
    tag_list = models.Tag.objects.all()
    order_5_list = models.Tag.objects.order_by('create_date')[:5]
    return render(request, 'index.html',{"article_list":article_list,
                                         "order_10_list":order_10_list,
                                         "tag_list":tag_list,
                                         "order_5_list":order_5_list})


def login_view(request):
    # html = """
    #
    # """
    #
    # return HttpResponse(html)
    return render(request, 'form.html')


def article(request):
    return HttpResponse('article')


def article_year(request, year, version):
    version_detail = "1.0.1"
    return HttpResponse('article %s %s %s' % (year, version, version_detail))


def article_detail(request, year, month, slug):
    return HttpResponse('article %s-%s %s' % (year, month, slug))


def article_archive(request, year, month):
    return HttpResponse('article 动态 %s-%s' % (year, month))


def article_archive3(request, arg1, arg2, slug):
    return HttpResponse('article 动态 %s-%s-%s' % (arg1, arg2, slug))


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def detail(request):
    # try:
    #     p = Poll.objects.get(pk=poll_id)
    # except Poll.DoesNotExist:
    #     raise Http404("Poll does not exist")
    context = {}
    context['hello'] = 'Hello World!'
    # return render(request, 'runoob.html', context)
    return render(request, 'try_python/my_site/html/mysheet.html')


def sql_test(request):
    conn = pymysql.connect(host='localhost', port=8889, user='root', passwd='root', db='data_structure')
    cursor = conn.cursor()  # 游标

    cursor.execute("select username, password from user;")

    data = cursor.fetchall()

    return HttpResponse(str(data))

    # conn = pymysql.connect(host='w.rdc.sae.sina.com.cn:3306', port=3306, user='n2o3n3x353', passwd='ijx1j43w5wmk4l1mmz134kzmwx25lw5ywxw3x0h2', db='app_tryprogram')
    # cursor = conn.cursor()  # 游标
    #
    # cursor.execute("select username, password from user;")
    #
    # data = cursor.fetchall()

def home_site(request,username, **kwargs):
    # 个人页面
    # print("username", username)
    user = models.Account.objects.filter(username=username).first()

    # 查询用户每一个tag对应的文章数
    # models.Tag.objects.values("pk").vannotate(c=Count("article__title")).values("title","c")

    # 查询用户每一个年月对应的文章数



    if not user:
        return render(request, "404.html")
    article_list = models.Article.objects.filter(account=user)
    account_info = models.Account.objects.get(username=username)
    if kwargs:
        condition=kwargs.get("condition")
        param=kwargs.get("param")

        if condition=="tag":
            article_list = article_list.filter(tags__name=param)
        # 时间标签
        else:
            year,month=param.split("-")
            article_list = article_list.filter(create_date__year=year,create_date__month=month)

    tag_list = models.Tag.objects.filter(account=user)
    return render(request, "home_site.html",{"user":user,
                                             "account_info":account_info,
                                             "article_list":article_list,
                                             "tag_list":tag_list})

def get_info_data(username):
    user = models.Account.objects.filter(username=username).first()
    account_info = models.Account.objects.get(username=username)
    tag_list = models.Tag.objects.filter(account=user)
    return {"user":user, "account_info":account_info, "tag_list":tag_list}


def article_view(request, username, article_id):
    # context = get_info_data(username)
    user = models.Account.objects.filter(username=username).first()
    account_info = models.Account.objects.get(username=username)
    tag_list = models.Tag.objects.filter(account=user)
    article_obj = models.Article.objects.filter(pk=article_id).first()

    comment_list=models.Comment.objects.filter(article_id=article_id)

    return render(request,"article_view.html", {"user":user,
                                                "account_info":account_info,
                                                "tag_list":tag_list,
                                                "article_obj":article_obj,
                                                "comment_list":comment_list})

def tag_view(request):
    tag_list = models.Tag.objects.all()
    order_5_list = models.Tag.objects.order_by('create_date')[:5]
    return render(request, "tagmatch_view.html",{"tag_list":tag_list,
                                            "order_5_list":order_5_list})

# 点赞视图
def digg(request):
    print(request.POST)

    article_id=request.POST.get("article_id")
    is_up=json.loads(request.POST.get("is_up"))
    user_id=request.user.pk  ###problem

    obj=models.ArticleUpdown.objects.filter(user_id=user_id,article_id=article_id).first()

    response={"stata":True}
    if not obj:
        ard=models.ArticleUpdown.objects.create(user_id=user_id,article_id=article_id,is_up=is_up)

        if is_up:
            models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)
        else:
            models.Article.objects.filter(pk=article_id).update(up_count=F("up_count")-1)
    else:
        response["stata"]=False

    return JsonResponse(response)


def comment(request):
    print(request.POST)

    article_id=request.POST.get("article_id")
    content = request.POST.get("content")
    pid = request.POST.get("pid")
    user_id = request.user.pk  ###problem

    comment_obj=models.Comment.objects.create(user_id=user_id,article_id=article_id,content=content,parent_comment_id=pid)

    response={}

    response["create_time"]=comment_obj.create_time.strftime("%Y-%m-%d %H:%m")
    response["username"]=comment_obj.user.username
    response["content"]=comment_obj.content
    if pid:
        response["pid"] = pid
        response["parent_comment_create_time"] = comment_obj.parent_comment.create_time
        response["parent_comment_username"] = comment_obj.parent_comment.user.username
        response["parent_comment_content"] = comment_obj.parent_comment.content
    print(response)
    return JsonResponse(response)

# @login_required
def my_edit(request):
    # article_list=models.Article.objects.filter(account=request.user)
    article_list = models.Article.objects.all()
    return render(request,"myedit.html",{"article_list":article_list})


def new_article(request):
    if request.method=="POST":
        title=request.POST.get("title")
        content=request.POST.get("content")

        models.Article.objects.create(title=title,content=content,user=request.user)
        return redirect("/myedit/")

    return render(request, 'new_article.html')