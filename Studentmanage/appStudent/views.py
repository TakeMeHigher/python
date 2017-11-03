from django.shortcuts import render,redirect
from app01 import  models
from django.core.paginator import Paginator
from app01.views import CheckLogin
# Create your views here.
@CheckLogin
def StudentList(request):
    # l=[]
    # for i in range(50):
    #     l.append(models.Student(sname="stu"+str(i),age=21,sex="male",email="stu@qq.com",phone="1478955",addr="北京",classes_id=2,headmaster_id=1))
    # models.Student.objects.bulk_create(l)

    studentlist=models.Student.objects.all()
    paginator=Paginator(studentlist,6)
    pageNums=paginator.num_pages
    num=request.GET.get("page",1)
    currentPage=int(num)
    if pageNums>9:
        if currentPage-5<1:
            page_range=range(1,10)
        elif currentPage+5>pageNums:
            page_range=range(currentPage-5,pageNums+1)
        else:
            page_range=range(currentPage-5,currentPage+5)
    else:
        page_range = paginator.page_range
    studentlist=paginator.page(num)
    return render(request,"StudentList.html",{"studentlist":studentlist,"page_range":page_range,"pageNums":pageNums,"currentPage":currentPage})



@CheckLogin
def StudentDetail(request):
    id=request.GET.get("id")
    student=models.Student.objects.filter(id=id)[0]
    return render(request,"StudentDetail.html",{"student":student})


@CheckLogin
def addStudent(request):
    if request.method=="POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        addr = request.POST.get("addr")
        cid = request.POST.get("cls")
        class_c=models.Class.objects.filter(id=cid)[0]
        headmaster=class_c.headmaster
        models.Student.objects.create(sname=name,age=age,sex=sex,email=email,phone=phone,addr=addr,classes_id=cid,headmaster=headmaster)

        return redirect("/appStudent/StudentList/")
    classes=models.Class.objects.all()
    headmasters=models.Headmaster.objects.all()
    return render(request,"addStiudent.html",{"classes":classes,"headmasters":headmasters})


@CheckLogin
def editStudent(request):
    if request.method=="POST":
        id=request.GET.get("id")
        name = request.POST.get("name")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        addr = request.POST.get("addr")
        cid = request.POST.get("cls")
        class_c = models.Class.objects.filter(id=cid)[0]
        headmaster = class_c.headmaster
        models.Student.objects.filter(id=id).update(sname=name, age=age, sex=sex, email=email, phone=phone, addr=addr,
                                      classes_id=cid, headmaster=headmaster)

        return redirect("/appStudent/StudentList/")

    id=request.GET.get("id")
    student=models.Student.objects.filter(id=id)[0]
    classes = models.Class.objects.all()
    headmasters = models.Headmaster.objects.all()
    return render(request,"editStudent.html",{"student":student,"classes":classes,"headmasters":headmasters})



def delStudent(request):
   id=request.GET.get("id")
   models.Student.objects.filter(id=id).delete()
   return redirect("/appStudent/StudentList/")

