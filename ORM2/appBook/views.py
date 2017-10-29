from django.shortcuts import render,HttpResponse,redirect
from appBook import models
# Create your views here.

def addBook(request):
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

        return redirect("/appBook/BookList/")

    publish_list=models.Publish.objects.all()
    author_list=models.Author.objects.all()
    return render(request,"addBook.html",{"publish_list":publish_list,"author_list":author_list})



def index(request):
    return render(request,"Dashboard.html")

def BookList(request):
    BookList=models.Book.objects.all()
    return render(request, "BookList.html", {"BookList":BookList})


def delBook(request):
    id=request.GET.get("id")
    models.Book.objects.get(id=id).delete()
    return redirect("/appBook/BookList/")



def editBook(request):
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
        return  redirect("/appBook/BookList/")

    publish_list = models.Publish.objects.all()
    author_list = models.Author.objects.all()
    id=request.GET.get("id")
    book=models.Book.objects.get(id=id)
    authors=book.authors.all()
    return render(request,"editBook.html",{"book":book,"publish_list":publish_list,"author_list":author_list,"authors":authors})