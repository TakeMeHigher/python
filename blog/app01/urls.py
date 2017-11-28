"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from django.conf import settings
from django.views.static import serve
urlpatterns = [
    url(r'^diggit/$', views.articleDiggit),
    url(r'^commentDigg/$', views.commentDigg),
    url(r'^buryit/$', views.articleBuryit),
    url(r'^comment/$', views.articleComment),
    url(r'^delComment/$', views.delComment),

    url(r'^commentTree/(?P<article_id>\d+)/$', views.commentTree),

    url(r'^(?P<username>.*)/p/(?P<article_id>[0-9]+)/$', views.articleDetail),

    url(r'^(?P<username>.*)/(?P<condition>tag|category|date)/(?P<para>.*)/$', views.homeSite),
    url(r'^(?P<username>.*)/$', views.homeSite),


]
