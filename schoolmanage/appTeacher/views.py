from django.shortcuts import render, redirect
from app01 import models
from app01.views import auth
from django.core.paginator import  Paginator

# Create your views here.
@auth
def TeacherList(request):
    # t=[]
    # for i in range(30):
    #     t.append(models.UserInfo(username="t"+str(i),password="123456",age=21,sex="f",email="stu@qq.com",ut_id=2,))
    # models.UserInfo.objects.bulk_create(t)
    teachers = models.UserInfo.objects.filter(ut_id=2).all()
    paginator=Paginator(teachers,6)
    num=request.GET.get("page",1)
    currentPage=int(num)
    pageNum=paginator.num_pages
    if pageNum>10:
        if currentPage-5<1:
            page_range=range(1,11)
        elif currentPage+5>pageNum:
            page_range=range(currentPage-5,pageNum+1)
        else:
            page_range=range(currentPage-5,currentPage+5)
    else:
        page_range=paginator.page_range
    teachers=paginator.page(num)
    return render(request, "TeacherList.html", {"teachers": teachers,"pageNum":pageNum,"page_range":page_range,"currentPage":currentPage})


from django.forms import Form
from django.forms import fields
from django.forms import widgets


class TeacherForm(Form):
    username = fields.CharField(required=True,
                                max_length=10,
                                error_messages={"required": "老师名称不能空","max_length":"老师名称长度不能大于10"
                                                },
                                widget=widgets.TextInput(attrs={"placeholder": "老师名称", "class": "form-control"}))
    password = fields.CharField(required=True,
                                min_length=6,
                                error_messages={"required": "密码不能为空","min_length":"密码长度不能小于6"},
                                widget=widgets.TextInput(attrs={"placeholder": "密码", "class": "form-control"}))

    email = fields.EmailField(required=True,
                              error_messages={"required": "邮箱不能为空","invalid":"邮箱格式不正确"},
                              widget=widgets.EmailInput(attrs={"placeholder": "邮箱", "class": "form-control"})
                              )
    sex = fields.ChoiceField(choices=[("m",'男'), ("f",'女')])

    age = fields.IntegerField(required=True,
                              error_messages={"required": "年龄不能为空"},
                              widget=widgets.TextInput(attrs={"placeholder": "年龄", "class": "form-control"})
                              )

    teacher_to_cls_id=fields.MultipleChoiceField(choices=models.ClassList.objects.values_list("id","caption"))


@auth
def addTeacher(request):
    if request.method == "GET":
        form = TeacherForm()

        return render(request, "addTeacher.html", {"form": form})
    else:
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.cleaned_data["ut_id"] = 2
            teacher_to_cls_id=form.cleaned_data["teacher_to_cls_id"]
            del form.cleaned_data["teacher_to_cls_id"]
            print(form.cleaned_data)
            teacher = models.UserInfo.objects.create(**form.cleaned_data)
            tc = []
            for id in teacher_to_cls_id:
                cls = models.ClassList.objects.filter(id=id)[0]
                tc.append(cls)
            teacher.teacher_to_cls.add(*tc)
            return redirect("/appTeacher/TeacherList/")
        return render(request, "addTeacher.html", {"form": form})


@auth
def editTeacher(request):
    if request.method=="GET":
        id=request.GET.get("id")
        teacher=models.UserInfo.objects.filter(id=id,ut_id=2).first()
        clss=teacher.teacher_to_cls.all()
        cls_ids=[cls.id for cls in clss ]
        form=TeacherForm(initial={"id":teacher.id,"username":teacher.username,"password":teacher.password,"email":teacher.email,"age":teacher.age,"sex":teacher.sex,"teacher_to_cls_id":cls_ids})
        return render(request,"editTeacher.html",{"form":form,"id":id})
    form=TeacherForm(request.POST)
    if form.is_valid():
         id=request.GET.get("id")
         print(id)
         teacher=models.UserInfo.objects.filter(id=id).first()
         form.cleaned_data["ut_id"]=2
         teacher_to_cls_id=form.cleaned_data["teacher_to_cls_id"]
         del form.cleaned_data["teacher_to_cls_id"]
         models.UserInfo.objects.filter(id=id).update(**form.cleaned_data)

         tc = []
         for id in teacher_to_cls_id:
             cls = models.ClassList.objects.filter(id=id)[0]
             tc.append(cls)
         print(tc)
         teacher.teacher_to_cls.clear()
         teacher.teacher_to_cls.add(*tc)
         return  redirect("/appTeacher/TeacherList/")
    else:
        render(request,"editTeacher.html",{"form":form})
@auth
def delTeacher(request):
    id = request.GET.get("id")
    models.UserInfo.objects.filter(id=id).delete()
    return redirect("/appTeacher/TeacherList/")
