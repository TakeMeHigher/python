from django.shortcuts import render,redirect
from app01 import models
from django.core.paginator import Paginator
# Create your views here.
def AuthorList(request):
    # authorlist=[]
    # for i in range(20):
    #     authorlist.append(models.Author(name="author"+str(i),age=i+20,addr="北京",phone="10086"))
    # models.Author.objects.bulk_create(authorlist)
    if request.user.is_authenticated():
        username = request.user.username
        authors=models.Author.objects.all()
        paginator = Paginator(authors, 3)
        num = request.GET.get("page", 1)
        pageNum = paginator.num_pages
        currentpage=int(num)
        if pageNum>5:
            if currentpage-5<1:
                page_range=range(1,11)
            elif currentpage+5>pageNum:
                page_range=range(currentpage-5,pageNum+1)
            else:
                page_range=range(currentpage-5,currentpage+5)
        else:
            page_range=paginator.page_range

        authors=paginator.page(num)
        return render(request,"authorList.html",{"authors":authors,"username":username,"page_range":page_range,"currentPage":currentpage,"pageNum":pageNum})
    else:
        return redirect("/login/")

def addAuthor(request):
    if request.user.is_authenticated():
        username=request.user.username
        if request.method=='POST':
            name=request.POST.get("name")
            age=request.POST.get("age")
            phone=request.POST.get("phone")
            addr=request.POST.get("addr")
            models.Author.objects.create(name=name,age=age,phone=phone,addr=addr)
            return redirect("/appAuthor/AuthorList/")

        return render(request,"addAuthor.html",locals())
    else:
        return redirect("/login/")

def editAuthor(request):
    if request.user.is_authenticated():
        username=request.user.username
        if request.method=="POST":
            id=request.GET.get("id")
            name = request.POST.get("name")
            age = request.POST.get("age")
            phone = request.POST.get("phone")
            addr = request.POST.get("addr")
            models.Author.objects.filter(id=id).update(name=name,age=age,phone=phone,addr=addr)
            return redirect("/appAuthor/AuthorList/")

        id=request.GET.get("id")
        author=models.Author.objects.get(id=id)
        return render(request,"editAuthor.html",locals())
    else:
        return redirect("/login/")


def delAuthor(request):
    if request.user.is_authenticated():
        id=request.GET.get("id")
        models.Author.objects.get(id=id).delete()
        return redirect("/appAuthor/AuthorList/")
    else:
        return redirect("/login/")

