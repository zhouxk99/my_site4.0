"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('register/',views.register),
    path('index/', views.index),
    path('logout/', views.logout),

    re_path('^$', views.index),
    path('tag/',views.tag_view),

    path('digg/',views.digg),
    path('comment/',views.comment),
    # path('delete_article/',views.delete_article),
    re_path('delete_article/(?P<article_id>\d+)$',views.delete_article),

    re_path('myedit/$',views.my_edit),
    re_path('myedit/newarticle/$',views.new_article),
    re_path('myedit/infoedit/',views.info),
    re_path('myedit/articleedit/(?P<article_id>\d+)$',views.article_edit),

    re_path('^(?P<username>\w+)$', views.home_site),
    re_path('^(?P<username>\w+)/(?P<condition>tag|archive)/(?P<param>.*)/$', views.home_site),
    re_path('tag/(?P<param>.*)/$', views.tag2_view),
    re_path('^(?P<username>\w+)/article/(?P<article_id>\d+)$', views.article_view),

    # re_path('search/(?P<param>.*)/$', views.searchresult)
    path('search/', views.searchresult)
]
