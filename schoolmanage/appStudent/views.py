from django.shortcuts import render,redirect,HttpResponse
from app01 import  models
from django.forms import Form,fields,widgets
from app01.views import auth
from django.core.paginator import Paginator
from rbac.baseUpdate import BasePagePermission
# Create your views here.

class StuForm(Form):
    name=fields.CharField(required=True,error_messages={"required":"学生名字不能为空"},
                          widget=widgets.TextInput(attrs={"placeholder": "学生姓名", "class": "form-control"})
                          )

    age=fields.IntegerField(required=True,error_messages={"required":"年龄不能为空","invalid":"年龄必须是数字"},
                          widget=widgets.TextInput(attrs={"placeholder": "年龄", "class": "form-control"})
                          )
    sex=fields.ChoiceField(choices=(("m","男"),("f","女")),initial=1,widget=widgets.Select)
    email=fields.EmailField(required=True,error_messages={"required":"邮箱不能为空","invalid":"邮箱格式不正确"},
                            widget=widgets.EmailInput(attrs={"placeholder": "邮箱", "class": "form-control"})
                            )
    cls_id=fields.ChoiceField(choices=[],widget=widgets.Select)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["cls_id"].choices=models.ClassList.objects.all().values_list("id","caption")

def StudentList(request):
    # s=[]
    # for i in range(50,100):
    #     s.append(models.Student(name="stu"+str(i),age=21,sex="f",email="stu"+str(i)+"@qq.com",cls_id=6))
    # models.Student.objects.bulk_create(s)
    students=models.Student.objects.all()
    paginator=Paginator(students,5)
    num=request.GET.get("page",1)
    pageNum=paginator.num_pages
    currentPage=int(num)
    if pageNum>10:
        if currentPage-5<0:
            page_range=range(1,11)
        elif currentPage+5>pageNum:
            page_range=range(currentPage-5,pageNum+1)
        else:
            page_range=range(currentPage-5,currentPage+5)
    else:
        page_range=paginator.page_range
    students=paginator.page(num)
    pagepermission = BasePagePermission(request.permission_code_list)
    return render(request,"StudentList.html",{"students":students,"pageNum":pageNum,"page_range":page_range,"currentPage":currentPage,"pagepermission":pagepermission})


def addStudent(request):
    if request.method=="GET":
        form=StuForm()
        print(form["cls_id"],"**********************")
        return render(request,"addStudent.html",{"form":form})
    form=StuForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        models.Student.objects.create(**form.cleaned_data)
        return redirect("/appStudent/StudentList/")
    return render(request,"addStudent.html",{"form":form})


def editStudent(request):
    if request.method=="GET":
        id=request.GET.get("id")
        stu=models.Student.objects.filter(id=id).first()
        clss=models.ClassList.objects.all()
        scls_id=stu.cls.id
        form=StuForm(initial={"name":stu.name,"sex":stu.sex,"age":stu.age,"email":stu.email,"cls_id":scls_id})
        return render(request,"editStudent.html",{"form":form,"clss":clss,"stu":stu})

    form=StuForm(request.POST)
    if form.is_valid():
        id=request.GET.get("id")
        print(form.cleaned_data)
        models.Student.objects.filter(id=id).update(**form.cleaned_data)
        return redirect("/appStudent/StudentList/")
    return render(request,"editStudent.html",{"form":form})



def delStudent(request):
    id=request.GET.get("id")
    print(id,"-------------------------")
    models.Student.objects.filter(id=id).delete()
    return HttpResponse("ok")