from django.shortcuts import render,redirect
from app01 import  models
# Create your views here.
from app01.views import CheckLogin

@CheckLogin
def TeacherList(request):
    TeacherList=models.Teacher.objects.all()
    return render(request, "TeacherList.html", {"TeacherList":TeacherList})


@CheckLogin
def TeacherDetail(request):
    id=request.GET.get("id")
    teacher= models.Teacher.objects.filter(id=id)[0]
    classes=models.Class.objects.filter(teachers=teacher)
    return render(request, "TeacherDetail.html", {"teacher": teacher,"classes":classes})

@CheckLogin
def addTeacher(request):
    if request.method=="POST":
        name=request.POST.get("name")
        pwd=request.POST.get("pwd")
        age=request.POST.get("age")
        sex=request.POST.get("sex")
        sal=request.POST.get("sal")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        addr=request.POST.get("addr")

        cids=request.POST.getlist("cls")
        print(cids)
        teacher=models.Teacher.objects.create(tname=name,pwd=pwd,age=age,sex=sex,sal=sal,email=email,phone=phone,addr=addr)
        for id in cids:
            cla_ss=models.Class.objects.filter(id=id)[0]
            print(cla_ss)
            cla_ss.teachers.add(teacher)
        return redirect("/appTeacher/TeacherList/")
    classes=models.Class.objects.all()
    return render(request,"addTeacher.html",{"classes":classes})

@CheckLogin
def editTeacher(request):
    if request.method=="POST":
        id=request.GET.get("id")
        print(id)
        name = request.POST.get("name")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        sal = request.POST.get("sal")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        addr = request.POST.get("addr")
        cids = request.POST.getlist("cls")
        print(cids)
        models.Teacher.objects.filter(id=id).update(tname=name, age=age, sex=sex, sal=sal, email=email, phone=phone,addr=addr)
        teacher=models.Teacher.objects.filter(id=id)[0]
        cls_l=[]
        for cid in cids:
            cla_ss = models.Class.objects.filter(id=cid)[0]
            cls_l.append(cla_ss)
        teacher.class_set.clear()
        teacher.class_set.add(*cls_l)
        return redirect("/appTeacher/TeacherList/")

    id=request.GET.get("id")
    teacher=models.Teacher.objects.filter(id=id)[0]
    tclasses = models.Class.objects.filter(teachers=teacher)
    classes=models.Class.objects.all()
    return render(request,"editTeacher.html",{"teacher":teacher,"tclasses":tclasses,"classes":classes})


@CheckLogin
def delTeacher(request):
    id=request.GET.get("id")
    models.Teacher.objects.filter(id=id).delete()
    return redirect("/appTeacher/TeacherList/")

