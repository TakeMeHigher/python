import re
from django.shortcuts import render,redirect,HttpResponse
from rbac import models
from rbac.service.init_permission import init_permission
def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user = models.User.objects.filter(username=user,password=pwd).first()
        print(request.POST)
        if not user:
            return render(request,'login.html')
        init_permission(user,request)
        return redirect('/index/')

class BasePagePermission(object):
    def __init__(self,code_list):
        self.code_list=code_list
    def has_add(self):
        if "add" in self.code_list:
            return True

    def has_edit(self):
        if "edit" in self.code_list:
            return True
    def has_del(self):
        if "del" in self.code_list:
            return  True

def index(request):

    return HttpResponse("aaaaa")


def userinfo(request):
    pagepermission = BasePagePermission(request.permission_code_list)
    data_list = [
        {'id': 1, 'name': 'xxx1'},
        {'id': 2, 'name': 'xxx2'},
        {'id': 3, 'name': 'xxx3'},
        {'id': 4, 'name': 'xxx4'},
        {'id': 5, 'name': 'xxx5'},
    ]
    return render(request,"userinfo.html",{"pagepermission":pagepermission,"data_list":data_list})


def userinfo_add(request):
    return render(request,"addUser.html")

def order(request):
    return HttpResponse('订单列表页面')

def order_add(request):
    return HttpResponse('添加订单页面')