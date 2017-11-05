from django.shortcuts import render,redirect
from app01 import models
from app01.views import auth
from django.forms import Form,fields,widgets
# Create your views here.

class HmForm(Form):
    username=fields.CharField(required=True,max_length=10,
                              error_messages={"required":"班主任名称不能为空","max_length":"名称长度能不能超过10"},
                              widget=widgets.TextInput(attrs={"placeholder": "班主任名称", "class": "form-control"})
                              )
    password=fields.CharField(required=True,min_length=6,
                              error_messages={"required":"密码不能为空","min_length":"密码长度不能小于6"},
                              widget=widgets.TextInput(attrs={"placeholder":"密码","class":"form-control"})
                              )

    age=fields.IntegerField(required=True,
                            error_messages={"required":"年龄不能为空","invalid":"年龄必须是数字"},
                            widget=widgets.TextInput(attrs={"placeholder":"年龄","class":"form-control"})
                            )
    email=fields.EmailField(required=True,
                            error_messages={"required":"邮箱不能为空","invalid":"邮箱格式不正确"},
                            widget=widgets.TextInput(attrs={"placeholder": "邮箱", "class": "form-control"})
                            )

    sex=fields.ChoiceField(choices=[("m","男"),("f","女")])

    cls_id=fields.MultipleChoiceField(choices=models.ClassList.objects.all().values_list("id","caption"))


@auth
def HeadMasterList(request):
    hms=models.UserInfo.objects.filter(ut_id=1).all()
    return render(request, "hmList.html",{"hms":hms})

@auth
def addHeadMaster(request):
    if request.method=="GET":
        form=HmForm()
        return render(request,"addHm.html",{"form":form})
    form=HmForm(request.POST)
    if form.is_valid():
        form.cleaned_data["ut_id"]=1
        cls_ids=form.cleaned_data["cls_id"]
        del form.cleaned_data["cls_id"]
        headmaster=models.UserInfo.objects.create(**form.cleaned_data)
        for id in cls_ids:
            models.ClassList.objects.filter(id=id).update(headmaster=headmaster)
        return redirect("/appHeadmaster/hmList/")
    return render(request,"addHm.html",{"form":form})





@auth
def editHeadMaster(request):
    if request.method=="GET":
        id=request.GET.get("id")
        hm=models.UserInfo.objects.filter(id=id).first()
        clss=hm.classlist_set.all()
        cls_id=[cls.id for cls in clss]
        form=HmForm(initial={"username":hm.username,"age":hm.age,"password":hm.password,
                             "sex":hm.sex,"email":hm.email,
                             "cls_id":cls_id
                             })
        return render(request,"editHm.html",{"form":form,"id":id})
    form=HmForm(request.POST)
    if form.is_valid():
        id=request.GET.get("id")

        form.cleaned_data["ut_id"]=1
        cls_ids=form.cleaned_data["cls_id"]
        print(cls_ids)
        del form.cleaned_data["cls_id"]
        models.UserInfo.objects.filter(id=id).update(**form.cleaned_data)
        headmaster=models.UserInfo.objects.filter(id=id).first()
        for id in cls_ids:
            models.ClassList.objects.filter(id=id).update(headmaster=headmaster)
        return redirect("/appHeadmaster/hmList/")
    return render(request,"addHm.html",{"form":form})

@auth
def delHeadMaster(request):
    id=request.GET.get("id")
    models.UserInfo.objects.filter(id=id).delete()
    return redirect("/appHeadmaster/hmList/")