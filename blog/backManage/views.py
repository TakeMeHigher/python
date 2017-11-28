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