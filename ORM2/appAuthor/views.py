from django.shortcuts import render,redirect
from appBook import models
# Create your views here.
def AuthorList(request):
    authors=models.Author.objects.all()
    return render(request,"authorList.html",{"authors":authors})

def addAuthor(request):
    if request.method=='POST':
        name=request.POST.get("name")
        age=request.POST.get("age")
        phone=request.POST.get("phone")
        addr=request.POST.get("addr")
        models.Author.objects.create(name=name,age=age,phone=phone,addr=addr)
        return redirect("/appAuthor/AuthorList/")

    return render(request,"addAuthor.html")


def editAuthor(request):
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
    return render(request,"editAuthor.html",{"author":author})

def delAuthor(request):
    id=request.GET.get("id")
    models.Author.objects.get(id=id).delete()
    return redirect("/appAuthor/AuthorList/")
