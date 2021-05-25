import datetime
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
import pymysql
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import F
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as D_login
from django.contrib.auth.models import User as D_User

from app01 import models
from django.conf import settings

@csrf_exempt
def login(request):
    error_msg = ''
    if request.session.get('is_login', None):  # 防止重复登录
        print('已经登陆')
        return redirect('/index/')
    if request.method == "POST":
        user = request.POST.get('user', None)  # 避免提交空，时异常
        pwd = request.POST.get('pwd', None)
        print(request.POST)
        obj = models.Account.objects.filter(username=user, password=pwd).first()
        user_auth = authenticate(request, username=user, password=pwd)
        print(user_auth)

        if user_auth is not None:
            D_login(request, user_auth)
            print("auth success")
            res = redirect("/index/")
            res.set_cookie('login_user', user_auth)
            request.session['is_login'] = True  # 往session字典内写入用户状态和数据
            request.session['user_id'] = user_auth.id
            request.session['user_name'] = user_auth.username
            return res
        #     return redirect("/")

        # if obj:
        #     print('user=' + user, 'pwd=' + pwd)
        #     user = models.Account.objects.get(username=user)
        #     res = redirect("/index/")
        #     res.set_cookie('login_user', user)
        #     request.session['is_login'] = True  # 往session字典内写入用户状态和数据
        #     request.session['user_id'] = user.id
        #     request.session['user_name'] = user.username
        #     return res
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
            d_user = D_User.objects.create_user(username=user, password=pwd, email=email)
            models.Account.objects.create(username=user, password=pwd, email=email)
            d_user.save()
            print('user=', user, 'pwd=', pwd, 'email=', email)
            success_msg = '注册成功！'
            return redirect('/login/', {'success_msg': success_msg})
    return render(request, 'register.html', {'error_msg': error_msg, 'success_msg': success_msg})


##########################################
def logout(request):
    if not request.session.get('is_login', None):  # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()  # 将session中的所有内容全部清空
    print("登出成功")
    return redirect('/index/')


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
    return render(request, 'index.html', {"article_list": article_list,
                                          "order_10_list": order_10_list,
                                          "tag_list": tag_list,
                                          "order_5_list": order_5_list})


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




def home_site(request, username, **kwargs):
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
        condition = kwargs.get("condition")
        param = kwargs.get("param")

        if condition == "tag":
            article_list = article_list.filter(tags__name=param)
        # 时间标签
        else:
            year, month = param.split("-")
            article_list = article_list.filter(create_date__year=year, create_date__month=month)

    tag_list = models.Tag.objects.all()
    return render(request, "home_site.html", {"user": user,
                                              "account_info": account_info,
                                              "article_list": article_list,
                                              "tag_list": tag_list})


def get_info_data(username):
    user = models.Account.objects.filter(username=username).first()
    account_info = models.Account.objects.get(username=username)
    tag_list = models.Tag.objects.all()
    return {"user": user, "account_info": account_info, "tag_list": tag_list}


def article_view(request, username, article_id):
    # context = get_info_data(username)
    user = models.Account.objects.filter(username=username).first()
    account_info = models.Account.objects.get(username=username)
    tag_list = models.Tag.objects.all()
    article_obj = models.Article.objects.filter(pk=article_id).first()

    comment_list = models.Comment.objects.filter(article_id=article_id)

    return render(request, "article_view.html", {"user": user,
                                                 "account_info": account_info,
                                                 "tag_list": tag_list,
                                                 "article_obj": article_obj,
                                                 "comment_list": comment_list})


def tag_view(request):
    tag_list = models.Tag.objects.all()
    order_5_list = models.Tag.objects.order_by('create_date')[:5]
    return render(request, "tagmatch_view.html", {"tag_list": tag_list,
                                                  "order_5_list": order_5_list})


def tag2_view(request, param):
    article_list = models.Article.objects.filter(tags__name=param)
    # order_5_list = models.Tag.objects.order_by('create_date')[:5]
    return render(request, "tagmatch2_view.html", {"article_list": article_list, })
    # "order_5_list":order_5_list})
    return HttpResponse("yes")


# 点赞视图
def digg(request):
    print(request.POST)

    article_id = request.POST.get("article_id")
    is_up = json.loads(request.POST.get("is_up"))
    user_id = request.user.pk  ###problem

    obj = models.ArticleUpdown.objects.filter(user_id=user_id, article_id=article_id).first()

    response = {"state": True}
    if not obj:
        ard = models.ArticleUpdown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)

        if is_up:
            models.Article.objects.filter(pk=article_id).update(up_count=F("up_count") + 1)
        else:
            models.Article.objects.filter(pk=article_id).update(up_count=F("up_count") - 1)
    else:
        response["state"] = False

    return JsonResponse(response)


def comment(request):
    print(request.POST)

    article_id = request.POST.get("article_id")
    content = request.POST.get("content")
    pid = request.POST.get("pid")
    user_id = request.user.pk  ###problem
    models.Article.objects.filter(pk=article_id).update(comment_count=F("comment_count") + 1)

    comment_obj = models.Comment.objects.create(user_id=user_id, article_id=article_id, content=content,
                                                parent_comment_id=pid)

    response = {}

    response["create_time"] = comment_obj.create_time.strftime("%Y-%m-%d %H:%m")
    response["username"] = comment_obj.user.username
    response["content"] = comment_obj.content
    if pid:
        response["pid"] = pid
        response["parent_comment_create_time"] = comment_obj.parent_comment.create_time
        response["parent_comment_username"] = comment_obj.parent_comment.user.username
        response["parent_comment_content"] = comment_obj.parent_comment.content
    # print(response)
    return JsonResponse(response)


@login_required
def my_edit(request):
    user_id = models.Account.objects.filter(username=request.user).first()
    article_list = models.Article.objects.filter(account_id=user_id)
    # article_list = models.Article.objects.all()
    # print(request.user)
    return render(request, "myedit.html", {"article_list": article_list})

@login_required
def new_article(request):
    error_msg = ''
    if request.method == "POST":
        title = request.POST.get("title")
        if not title:
            error_msg = 'title!'
        tag = request.POST.get("tag")
        describe = request.POST.get("describe")
        content = request.POST.get("content")
        user_id = models.Account.objects.filter(username=request.user).first()
        # print(tag)
        if title and content:
            if tag:
                print(111222333)
                aa = models.Tag.objects.filter(name=tag).first()
                if not aa:
                    aa = models.Tag.objects.create(name=tag)
                    # tag = models.Tag.objects.filter(name=tag).first()
            else:
                tag = 'blank'
                aa = models.Tag.objects.filter(name=tag).first()
                print(tag)
            # if not describe:
            #     describe = content
            #     if len(content) > 33:
            #         describe = describe.slice(33)
            models.Article.objects.create(title=title, tags=aa, content=content, decsribe=describe, account=user_id)
            return redirect("/myedit/")
        else:
            print('error')
            error_msg = '标题与文章不能为空！'
            # return redirect("/myedit/newarticle", {"error_msg": error_msg})
        # models.Article.objects.create(title=title, tags_id=tag, decsribe=describe, content=content, account=user_id)

    return render(request, 'new_article.html', {'error_msg': error_msg})



def delete_article(request, article_id):
    # print(request.POST)
    # if request.method == 'POST':
    #     id=request.POST.get("article_id")
    article = models.Article.objects.get(pk=article_id)
    article.delete()

    return redirect("/myedit/")


def article_edit(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    print(request.POST)
    if request.method == "POST":
        article.title = request.POST.get("title")
        article.content = request.POST.get("content")
        article.decsribe = request.POST.get("describe")
        article.save()
        return redirect("/myedit/")

    return render(request, 'article_change.html', {"article": article})

# def searchresult(request,param):
#     if models.Article.objects.filter(title=param).first():
#         type = 'article'
#         text = models.Article.objects.filter(title=param)
#     elif models.Tag.objects.filter(name=param):
#         type = 'tag'
#         tag_name = models.Tag.objects.filter(name=param).first()
#         text = models.Article.objects.filter(tags=tag_name)
#     else:
#         type = 'none'
#         text = 'none'
#
#     return render(request, 'searchresult.html', {'type':type,'text':text})

def searchresult(request):
    tag_list = models.Tag.objects.all()
    order_5_list = models.Tag.objects.order_by('create_date')[:5]
    param = request.GET.get('search')
    if models.Article.objects.filter(title=param).first():
        type = 'article'
        text = models.Article.objects.filter(title=param)
    elif models.Tag.objects.filter(name=param):
        type = 'tag'
        tag_name = models.Tag.objects.filter(name=param).first()
        text = models.Article.objects.filter(tags=tag_name)
    else:
        type = 'none'
        text = 'none'


    return render(request, 'searchresult.html', {'type':type,'text':text,
                                                 "tag_list": tag_list,
                                                 "order_5_list": order_5_list})
@login_required
def info(request):
    user = models.Account.objects.filter(username=request.user).first()
    if request.method == "POST":
        user.email = request.POST.get("email")
        user.signature = request.POST.get("signature")
        user.save()
        return redirect("/myedit/")
    return render(request,'info.html',{'user':user})