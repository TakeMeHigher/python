from django.shortcuts import render,redirect,HttpResponse
from app01 import  models
from app01.forms import ArticleForm
import datetime
import os,json
from django.conf import settings
# Create your views here.
#个人博客管理后台页面
def personalManage(request,username):
    return render(request,"personalManage.html")

#添加文章
def addArticle(request):
    user_id=request.user.id
    if request.method=="POST":
        form =ArticleForm(user_id,request.POST)
        print(form)
        if form.is_valid():
            create_time=datetime.datetime.now()
            data=form.cleaned_data
            title=data.get("title")
            tag_ids=data.pop("tag_ids")
            content=data.get("content")
            category_id=data.get("category_id")
            desc=data.get("content")[:30]
            siteArticleCategory_id=data.get("siteArticleCategory_id")
            # print(data.get("title"))
            # print(data.get("desc"))
            # print(data.get("category_id"))
            # print(data.get("tag_ids"))
            # print(data.get("siteArticleCategory_id"))
            article=models.Article.objects.create(title=title,desc=desc,category_id=category_id,siteArticleCategory_id=siteArticleCategory_id,user_id=user_id)
            models.ArticleDetail.objects.create(article=article,content=content)
            return render(request,"updateSuccess.html")

        return render(request,"addArticle.html",{"form":form})
    form=ArticleForm(user_id)
    return render(request,"addArticle.html",{"form":form})


#上传文件
def uploadFile(request):
    print(request.POST)
    print(request.FILES,"--------------")
    file_obj=request.FILES.get("imgFile")
    filename=file_obj.name
    path=os.path.join(settings.MEDIA_ROOT,"article_uploads",filename)
    with open(path,"wb")as f:
        for i in file_obj:
            f.write(i)
    response = {
        "error": 0,
        "url": "/media/article_uploads/" + filename + "/"

    }
    return HttpResponse(json.dumps(response))

#删除文章
def delArticle(request):
    article_id=request.POST.get("article_id")
    models.Article.objects.filter(id=article_id).delete()

    return HttpResponse("ok")

#后台文章分类展示
def articleCategory(request,category_title):
    print(category_title,"------------------")
    articles=models.Article.objects.filter(user=request.user,category__title=category_title).all()
    print(articles)
    return render(request,"backArticleCategory.html",{"articles":articles})

#分类操作首页
def categotyEdit(request):
    return render(request,"categoryEdit.html")

#添加分类
def addCategory(request):
    title=request.POST.get("title")
    add_response={"flag":False,"error":None,"category_id":None,"category_title":None}
    category=models.Category.objects.filter(title=title)
    if not category:
        blog=models.Blog.objects.filter(user=request.user).first()
        category= models.Category.objects.create(blog=blog,title=title)
        add_response["flag"]=True
        add_response["category_id"]=category.id
        add_response["category_title"]=category.title
    else:
        add_response["error"]="当前分类已存在"
    print(add_response)
    return HttpResponse(json.dumps(add_response))

#删除分类
def delCategory(request):
    id=request.GET.get("id")
    models.Category.objects.filter(id=id).delete()
    return HttpResponse("ok")

#编辑分类
def editCategory(request):
    id=request.POST.get("id")
    title=request.POST.get("title")
    print(id,'--------')
    print(title,'-----')
    models.Category.objects.filter(id=id).update(title=title)
    return  HttpResponse("ok")