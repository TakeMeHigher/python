from django.shortcuts import render,redirect
from app01 import  models
# Create your views here.

def CheckLogin(fun):
    def inner(request,*args,**kwargs):
        isLogin = request.session.get("isLogin")
        if isLogin:
            ret=fun(request,*args,**kwargs)
            return ret
        else:
            return redirect("/login/")
    return inner

@CheckLogin
def index(request):
    return render(request, "Dashboard.html")


def login(request):
    msg=""
    if request.method=="POST":
        username=request.POST.get("user")
        pwd=request.POST.get("pwd")
        headmaster=models.Headmaster.objects.filter(hname=username,pwd=pwd)
        teacher=models.Teacher.objects.filter(tname=username,pwd=pwd)
        if headmaster or teacher:
            request.session["isLogin"] = True
            request.session["username"]=username
            return redirect("/index/")

        else:
            msg="用户名或密码错误"

    return render(request,"login.html",{"msg":msg})

def logout(request):
    request.session.flush()
    return redirect("/login/")




