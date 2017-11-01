from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# Create your views here.

def addBook(request):
    if request.user.is_authenticated():
        username=request.user.username
        if request.method=="POST":
            title=request.POST.get("title")
            PublishDate=request.POST.get("PublishDate")
            publish_id=request.POST.get("publish")
            authors_id=request.POST.getlist("authors")
            price=request.POST.get("price")
            publish=models.Publish.objects.get(id=publish_id)
            book_obj=models.Book.objects.create(title=title,publishDate=PublishDate,publish=publish,price=price)
            authorList=[]
            print(authors_id)
            for authorid in authors_id:
                author=models.Author.objects.get(id=authorid)
                authorList.append(author)
            print(authorList)
            book_obj.authors.add(*authorList)
            return redirect("/app01/BookList/")

        publish_list=models.Publish.objects.all()
        author_list=models.Author.objects.all()
        return render(request,"addBook.html",{"publish_list":publish_list,"author_list":author_list,"username":username})
    else:
        return redirect("/login/")



def index(request):
    if request.user.is_authenticated():
        username=request.user.username
        return render(request,"Dashboard.html",{"username":username})
    else:
        return redirect("/login/")


def BookList(request):
    # boolist=[]
    # for i in range(30):
    #    boolist.append( models.Book(title="book"+str(i),publishDate="2017-02-14",price=254,publish_id=2))
    # models.Book.objects.bulk_create(boolist)
    if request.user.is_authenticated():
        username=request.user.username
        BookList=models.Book.objects.all()
        paginator=Paginator(BookList,5)
        num = request.GET.get("page", 1)
        currentPage=int(num)
        pageNum = paginator.num_pages
        if pageNum>10:
            if currentPage-5<1:
                page_range=range(1,11)
            elif currentPage+5>pageNum:
                page_range=range(currentPage-5,pageNum+1)
            else:
                page_range=range(currentPage-5,currentPage+5)
        else:
            page_range = paginator.page_range

        BookList=paginator.page(num)
        return render(request, "BookList.html", {"BookList":BookList,"username":username,"page_range":page_range,"num":int(num),"pageNum":pageNum})
    else:
        return redirect("/login/")



def delBook(request):
    if request.user.is_authenticated():
        id=request.GET.get("id")
        models.Book.objects.get(id=id).delete()
        return redirect("/app01/BookList/")
    else:
        return redirect("/login/")




def editBook(request):
    if request.user.is_authenticated():
        username=request.user.username
        if request.method=="POST":
            id=request.GET.get("id")
            title = request.POST.get("title")
            PublishDate = request.POST.get("PublishDate")
            publish_id = request.POST.get("publish")
            authors_id = request.POST.getlist("authors")
            price = request.POST.get("price")
            publish = models.Publish.objects.get(id=publish_id)
            book_obj=models.Book.objects.get(id=id)
            models.Book.objects.filter(id=id).update(title=title, publishDate=PublishDate, publish=publish, price=price)
            authorList = []
            print(authors_id)
            for authorid in authors_id:
                author = models.Author.objects.get(id=authorid)
                authorList.append(author)
            print(authorList)
            book_obj.authors.clear()
            book_obj.authors.add(*authorList)
            return  redirect("/app01/BookList/")

        publish_list = models.Publish.objects.all()
        author_list = models.Author.objects.all()
        id=request.GET.get("id")
        book=models.Book.objects.get(id=id)
        authors=book.authors.all()
        return render(request,"editBook.html",{"book":book,"publish_list":publish_list,"author_list":author_list,"authors":authors,"username":username})
    else:
        return redirect("/login/")

def Login(request):
    if request.method=="POST":
        username=request.POST.get("user")
        password=request.POST.get("pwd")
        user=authenticate(username=username,password=password)
        if user:
            #cookie
            # obj=redirect("/app01/index/")
            # obj.set_cookie("islogin",True,max_age=60)
            # obj.set_cookie("username",username)
            # return obj
            #session
             # request.session["islogin"]=True
             # request.session["username"]=username
             # return render(request,"Dashboard.html",{"username":username})

            login(request,user)
            return redirect("/app01/index/")

        else:
            return redirect("/login/")
    return render(request,"login.html")


def Logout(request):
    # request.session.flush()
    logout(request)
    return redirect("/login/")


def changpwd(request):
    if request.user.is_authenticated():
        user=request.user
        state=""
        if request.method=="POST":
            oldpwd=request.POST.get("oldpwd")
            newpwd=request.POST.get("newpwd")
            repeatpwd=request.POST.get("repeatpwd")
            if user.check_password(oldpwd):
                if not newpwd:
                    state="newpwd is null"
                elif newpwd!=repeatpwd:
                    state="newpwd和repeatpwd不一样"
                else:
                    user.set_password(newpwd)
                    user.save()
                    return redirect("/login/")
            else:
                state="oldpwd is error"


        return render(request,"changpwd.html",{"state":state})
    else:
        return redirect("/login/")

def reg(request):
    state=""
    if request.method=="POST":
        username=request.POST.get("username")
        pwd=request.POST.get("pwd")
        email=request.POST.get("email")
        if User.objects.filter(username=username):
            state="用户名已经被注册"
        elif username=="" or pwd=="":
            state="用户名或密码不能为空"
        else:
            new_user=User.objects.create_user(username=username,password=pwd,email=email)
            new_user.save()
            return redirect("/login/")

    return render(request,"reg.html",{"state":state})