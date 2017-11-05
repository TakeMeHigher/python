from django.shortcuts import render,redirect
from app01 import models
from app01.views import auth
from django.forms import Form
from django.forms import fields
from django.forms import  widgets
# Create your views here.
@auth
def ClassList(request):
    clss=models.ClassList.objects.all()

    return render(request,"ClassList.html",{"clss":clss})


class ClassForm(Form):
    caption=fields.CharField(required=True,error_messages={"required":"班级名称不能为空"},
                             widget=widgets.TextInput(attrs={"placeholder":"班级名称","class":"form-control"})
                             )

    headmaster_id=fields.ChoiceField(choices=models.UserInfo.objects.filter(ut_id=1).all().values_list("id","username"),
                                     widget=widgets.Select)

    teacher_ids=fields.MultipleChoiceField(choices=models.UserInfo.objects.filter(ut_id=2).all().values_list("id","username"))

@auth
def editClass(request):
    if request.method=="GET":
        id=request.GET.get("id")
        cls=models.ClassList.objects.filter(id=id).first()
        headmaster_id=cls.headmaster.id
        teachers=cls.userinfo_set.filter(ut_id=2).all()
        teacher_ids= [teacher.id for teacher in teachers]
        print(teacher_ids)
        form = ClassForm(initial={"caption":cls.caption,"headmaster_id":headmaster_id,"teacher_ids":teacher_ids})
        return render(request,"editClass.html",{"form":form,"id":id})
    form=ClassForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        id=request.GET.get("id")
        teacher_ids=form.cleaned_data["teacher_ids"]
        del form.cleaned_data["teacher_ids"]
        print(form.cleaned_data)
        models.ClassList.objects.filter(id=id).update(**form.cleaned_data)
        cls=models.ClassList.objects.filter(id=id).first()
        cls.userinfo_set.clear()
        t_l = []
        for id in teacher_ids:
            t_l.append(models.UserInfo.objects.filter(id=id, ut_id=2).first())

        for teacher in t_l:
            teacher.teacher_to_cls.add(cls)
        return redirect("/appClass/ClassList/")

@auth
def addClass(request):
    if request.method=="GET":
        form=ClassForm()
        return render(request,"addClass.html",{"form":form})
    form=ClassForm(request.POST)

    if form.is_valid():
        teacherids=form.cleaned_data["teacher_ids"]
        del form.cleaned_data["teacher_ids"]
        cls=models.ClassList.objects.create(**form.cleaned_data)
        t_l=[]
        for id in teacherids:
            t_l.append(models.UserInfo.objects.filter(id=id,ut_id=2).first())

        for teacher in t_l:
            teacher.teacher_to_cls.add(cls)

        return redirect("/appClass/ClassList/")
    return render(request,"addClass.html",{"form":form})
@auth
def delClass(request):
    id=request.GET.get("id")
    models.ClassList.objects.filter(id=id).delete()
    return redirect("/appClass/ClassList/")