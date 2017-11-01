from django.shortcuts import render,redirect
from app01 import models
from django.core.paginator import Paginator
# Create your views here.
def PublishList(request):
    # publishlist=[]
    # for i in range(20):
    #     publishlist.append(models.Publish(name="出版社"+str(i),addr="北京"))
    # models.Publish.objects.bulk_create(publishlist)
    if request.user.is_authenticated():
        username = request.user.username
        publishList=models.Publish.objects.all()
        paginator=Paginator(publishList,3)
        num=request.GET.get("page",1)
        pageNum=paginator.num_pages
        currentPage=int(num)
        if pageNum>10:
            if currentPage-5<1:
                page_range=range(1,11)
            elif currentPage+5>pageNum:
                page_range=range(currentPage-5,pageNum+1)
            else:
                page_range=range(currentPage-5,currentPage+5)
                
        else:
            page_range = paginator.page_range
        publishList=paginator.page(num)
       
        return render(request,"publishList.html",{"publishList":publishList,"username":username,"page_range":page_range,"currentPage":currentPage,"pageNum":pageNum})
    else:
        return redirect("/login/")

def addPublish(request):
    if request.user.is_authenticated():
        username=request.user.username
        if request.method=="POST":
            name=request.POST.get("name")
            addr=request.POST.get("addr")
            models.Publish.objects.create(name=name,addr=addr)
            return redirect("/appPublish/PublishList")
        return render(request,"addPublish.html",locals())
    else:
        return redirect("/login/")



def editPublish(request):
    if request.user.is_authenticated():
        username=request.user.username
        if request.method=="POST":
            id=request.GET.get("id")
            name = request.POST.get("name")
            addr = request.POST.get("addr")
            models.Publish.objects.filter(id=id).update(name=name,addr=addr)
            return redirect("/appPublish/PublishList")
        id=request.GET.get("id")
        publishObj=models.Publish.objects.get(id=id)
        return render(request,"editPublish.html",locals())
    else:
        return redirect("/login/")


def delPublish(request):
    if request.user.is_authenticated():
        id=request.GET.get("id")
        models.Publish.objects.get(id=id).delete()
        return redirect("/appPublish/PublishList")
    else:
        return redirect("/login/")
