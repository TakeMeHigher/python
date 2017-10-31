from django.shortcuts import render,redirect
from appBook import models
# Create your views here.
def PublishList(request):
    publishList=models.Publish.objects.all()
    return render(request,"publishList.html",{"publishList":publishList})

def addPublish(request):
    if request.method=="POST":
        name=request.POST.get("name")
        addr=request.POST.get("addr")
        models.Publish.objects.create(name=name,addr=addr)
        return redirect("/appPublish/PublishList")
    return render(request,"addPublish.html")

def editPublish(request):
    if request.method=="POST":
        id=request.GET.get("id")
        name = request.POST.get("name")
        addr = request.POST.get("addr")
        models.Publish.objects.filter(id=id).update(name=name,addr=addr)
        return redirect("/appPublish/PublishList")
    id=request.GET.get("id")
    publishObj=models.Publish.objects.get(id=id)
    return render(request,"editPublish.html",{"publishObj":publishObj})

def delPublish(request):
    id=request.GET.get("id")
    models.Publish.objects.get(id=id).delete()
    return redirect("/appPublish/PublishList")