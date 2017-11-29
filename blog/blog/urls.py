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
from app01.views import pcgetcaptcha,pcajax_validate
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    #url(r'^login/', views.login),
    url(r'^reg/', views.reg),
    url(r'^$', views.index),
    url(r'^get_valid_Code_img/', views.get_valid_Code_img),
    url(r'^logout/', views.logout),
    url(r'^changePassword/', views.changePassword),

    url(r'^cate/(?P<site_article_category>.*)/$', views.index),  # # index(requset,site_article_category=python)


    #个人站点首页
    url(r'^blog/',include("app01.urls") ),
    url(r'^backManage/',include("backManage.urls") ),

    #media配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # 滑动验证码配置

    url(r'^pc-geetest/register', pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^pc-geetest/ajax_validate', pcajax_validate, name='pcajax_validate'),

]
