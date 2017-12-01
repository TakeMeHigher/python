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
from backManage import views
from django.conf import settings
from django.views.static import serve
urlpatterns = [

    url(r'^(?P<username>.*)/manage/$', views.personalManage),
    url(r'^delArticle/$', views.delArticle),
    url(r'^addArticle/$', views.addArticle),
    url(r'^editArticle/$', views.editArticle),
    url(r'^uploadFile/$', views.uploadFile),
    url(r'^categotyEdit/$', views.categotyEdit),
    url(r'^articleCategory/(?P<category_title>.*)/$', views.articleCategory),

    url(r'^addCategory/$', views.addCategory),
    url(r'^delCategory/$', views.delCategory),
    url(r'^editCategory/$', views.editCategory),



]
