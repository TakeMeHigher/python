from django.shortcuts import render,redirect
from app01 import models
# Create your views here.

def ClassList(request):
    isLogin = request.session.get("isLogin")
    username = request.session.get("username")
    if isLogin:
        classes=models.Class.objects.all()
        teachers=models.Teacher.objects.all()
        return render(request, "ClassList.html", {"username":username, "classes":classes, "teachers":teachers})
    else:
        return redirect("/app01/login/")

def addClass(request):
    isLogin = request.session.get("isLogin")
    username = request.session.get("username")
    if isLogin:
        if request.method=="POST":
            name=request.POST.get("name")
            teacher_ids=request.POST.getlist("teacher")
            headmaster_id=request.POST.get("headmaster")
            headmaster=models.Headmaster.objects.filter(id=headmaster_id)[0]
            class_es=models.Class.objects.create(cname=name,headmaster=headmaster)

            teacher_l=[]
            for id in teacher_ids:
                teacher=models.Teacher.objects.filter(id=id)[0]
                teacher_l.append(teacher)
            class_es.teachers.add(*teacher_l)
            return redirect("/appClass/ClassList")

        headmasters=models.Headmaster.objects.all()
        teachers = models.Teacher.objects.all()
        return render(request,"addClass.html",{"headmasters":headmasters,"teachers":teachers,"username":username})
    else:
        return redirect("/app01/login/")

def editClass(request):
    isLogin = request.session.get("isLogin")
    username = request.session.get("username")
    if isLogin:
        if request.method=="POST":
            id=request.GET.get("id")
            name = request.POST.get("name")
            teacher_ids = request.POST.getlist("teacher")
            headmaster_id = request.POST.get("headmaster")
            headmaster = models.Headmaster.objects.filter(id=headmaster_id)[0]
            models.Class.objects.filter(id=id).update(cname=name, headmaster=headmaster)
            class_c=models.Class.objects.filter(id=id)[0]
            teacher_l = []
            for id in teacher_ids:
                teacher = models.Teacher.objects.filter(id=id)[0]
                teacher_l.append(teacher)
            class_c.teachers.clear()
            class_c.teachers.add(*teacher_l)
            return redirect("/appClass/ClassList")
        id=request.GET.get("id")
        class_c=models.Class.objects.filter(id=id)[0]
        cteachers=class_c.teachers.all()
        teachers=models.Teacher.objects.all()
        headmasters = models.Headmaster.objects.all()
        return render(request,"editClass.html",{"cteachers":cteachers,"teachers":teachers,"headmasters":headmasters,"class_c":class_c,"username":username})

    else:
        return redirect("/app01/login/")


def delClass(request):
    isLogin = request.session.get("isLogin")
    username = request.session.get("username")
    if isLogin:
        id=request.GET.get("id")
        models.Class.objects.filter(id=id).delete()
        return redirect("/appClass/ClassList")
    else:
        return redirect("/app01/login/")

