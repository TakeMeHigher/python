from django.shortcuts import render,redirect
from app01 import models
from django.forms import Form
from django.forms import fields
from django.forms import  widgets
# Create your views here.

class LoginForm(Form):
    username=fields.CharField(required=True,error_messages={"require":"用户名不能为空"},
                              widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"用户名"}))

    password=fields.CharField(required=True,error_messages={"require":"密码不能为空"},
                              widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"密码"}))


# def login(request):
#     if request.method=="GET":
#         return render(request,"login.html")
#     elif request.method=="POST":
#         name=request.POST.get("user")
#         pwd=request.POST.get("pwd")
#         user=models.UserInfo.objects.filter(username=name,password=pwd)[0]
#         if user:
#             request.session["userinfo"]={"id":user.id,"username":user.username}
#             return redirect("/index/")
#         else:
#             return render(request,"login.html",{"msg":"用户名或密码错误!"})
#     else:
#         return render(request,"login.html",{"msg":"请求方式不对"})

def login(request):
    if request.method=="GET":
        form =LoginForm()
        return render(request,"login.html",{"form":form})
    form=LoginForm(request.POST)
    if form.is_valid():
        request.session["userinfo"]={"username":form.cleaned_data["username"],"password":form.cleaned_data["password"]}
        return redirect("/index/")
def auth(fun):
    def inner(request,*args,**kwargs):
        userinfo=request.session.get("userinfo")
        if userinfo:
            ret=fun(request,*args,**kwargs)
            return ret
        else:
            return redirect("/login/")
    return  inner

@auth
def index(request):
    return render(request,"Dashboard.html")

@auth
def logout(request):
    request.session.flush()
    return redirect("/login/")

@auth
def changpwd(request):
    if request.method=="GET":
        return render(request,"changpwd.html")
    oldpwd=request.POST.get("oldpwd")
    newpwd=request.POST.get("newpwd")
    repeatpwd=request.POST.get("repeatpwd")
    username=request.session["userinfo"]["username"]
    pwd=request.session["userinfo"]["password"]


    if pwd==oldpwd:
        if not newpwd:
            msg="新密码不能为空"
            return render(request, "changpwd.html", {"msg": msg})
        elif newpwd !=repeatpwd:
            msg="两次输入的密码不一致"
            return render(request, "changpwd.html", {"msg": msg})
        else:
            models.UserInfo.objects.filter(username=username, password=pwd).update(password=newpwd)
            return redirect("/login/")

    msg="原密码输入错误"
    return render(request, "changpwd.html", {"msg": msg})

