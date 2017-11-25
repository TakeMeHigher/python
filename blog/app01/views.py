from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from app01 import models
from app01.forms import RegForm
from django.db.models import  F
from django.core.paginator import Paginator
import json
import random

# Create your views here.

# def auth(fun):
#     def inner(request,*args,**kwargs):
#         if request.user.is_authenticated():
#             ret=fun(request,*args,**kwargs)
#             return ret
#         else:
#             return  redirect("/login/")
#     return inner



#登录
def login(request):
    if request.method=="POST":
        name = request.POST.get("name")
        pwd = request.POST.get("pwd")
        valid_Code=request.POST.get('valid_Code')
        print(valid_Code)
        login_dic = {"is_login": False,"msg":None}
        if valid_Code.upper()==request.session.get('valid_str').upper():
            #user = models.Userinfo.objects.filter(username=name, password=pwd).first()
            user=auth.authenticate(username=name,password=pwd)
            print(name,pwd)
            if user:
                #request.session['user']={"username":name,'id':user.id}
                auth.login(request,user)
                #request.session["username"] = name
                login_dic["flag"] = True
            else:
                login_dic['msg']='用户名或密码错误'
        else:
            login_dic['msg']='验证码错误'

        return HttpResponse(json.dumps(login_dic))


    return  render(request,'login.html')

#注册
def reg(request):
    if request.method=="POST":
       form=RegForm(data=request.POST,files=request.FILES)
       reg_dic={"flag":False,"error":None}
       if form.is_valid():
           reg_dic['flag']=True
           avatar=request.FILES.get('avatar')
           form.cleaned_data['avatar']=avatar
           confirmPassword=form.cleaned_data.pop('confirmPassword')
           print(form.cleaned_data)
           models.Userinfo.objects.create_user(**form.cleaned_data)
       reg_dic['error']=form.errors
       print(reg_dic)
       return  HttpResponse(json.dumps(reg_dic))

    form=RegForm()
    return render(request,'reg.html',{'form':form})

#首页
def index(request,*args,**kwargs):
    if kwargs:
        articles=models.Article.objects.filter(siteArticleCategory__name=kwargs.get("site_article_category"))
    else:
        articles = models.Article.objects.all()

    SiteCategory=models.SiteCategory.objects.all()

    paginator=Paginator(articles,5)
    page_nums=paginator.num_pages
    num=request.GET.get("page",1)
    currentPage=int(num)

    if page_nums>5:
        if currentPage-2<1:
            page_range=range(1,6)
        elif currentPage+2>page_nums:
            page_range=range(currentPage-2,page_nums+1)
        else:
            page_range=range(currentPage-2,currentPage+2)
    else :
        page_range=paginator.page_range

    articles=paginator.page(num)

    return render(request,'index.html',{"SiteCategory":SiteCategory,"articles":articles,"pageNum":page_nums,"page_range":page_range,"currentPage":currentPage})


#注销
def logout(request):
    request.session.flush()
    return redirect('/login/')


#修改密码
def changePassword(request):
    user=request.user
    if request.method=="POST":
        newpwd=request.POST.get("newpwd")
        oldpwd=request.POST.get("oldpwd")
        repeatpwd=request.POST.get("repeatpwd")
        cp_dic={"flag":False,"errors":None}
        if user.check_password(oldpwd):
            if newpwd:
                if repeatpwd:
                    if newpwd==repeatpwd:
                        cp_dic['flag']=True
                        user.set_password(newpwd)
                        user.save()
                        print(user.password)
                    else:
                        cp_dic["errors"] = "两次输入密码不一致"

                else:
                    cp_dic["errors"]="确认密码不能为空"
            else:
                cp_dic["errors"]="新密码不能为空"

        else:
            cp_dic["errors"]="原密码输入错误"

        return HttpResponse(json.dumps(cp_dic))



    return render(request, "changePassword.html")




#--------------------------------------------------------验证码-------------------------------------------------

#生成随机颜色
def getRandomColor():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

#生成随机字母和数字
def getRandomCharNum():
    random_num = str(random.randint(0, 9))
    random_lower = chr(random.randint(65, 90))
    random_upper = chr(random.randint(97, 122))
    random_char = random.choice([random_num, random_lower, random_upper])
    #一次只返回一个字符
    return random_char

#生成干扰线
def getLine(width,height):
    x1 = random.randint(0, width)
    y1 = random.randint(0, height)
    x2 = random.randint(0, width)
    y2 = random.randint(0, height)

    return (x1, y1, x2, y2)

#生成随机验证码
def get_valid_Code_img(request):
    from io import BytesIO
    from PIL import  Image,ImageDraw,ImageFont

    # #图片
    img=Image.new(mode='RGB',size=(80,34),color=getRandomColor())
    # #图片内容
    draw=ImageDraw.Draw(im=img,mode='RGB')
    # #图片的字体
    font=ImageFont.truetype(font='app01/static/font/kumo.ttf',size=25)
    valid_list=[]
    for i in range(5):
        random_char=getRandomCharNum()
        #加文本
        draw.text((i*15,8),random_char,fill=getRandomColor(),font=font)
        #加干扰线
        draw.line(getLine(80,34),fill=getRandomColor())
        valid_list.append(random_char)


    valid_str=''.join(valid_list)
    f = BytesIO()
    img.save(f,'png')
    data=f.getvalue()

    request.session['valid_str']=valid_str
    return HttpResponse(data)



#-----------------------------------------------------验证码结束-----------------------------------------------


#-----------------------------------------------------文章部分---------------------------------------------------
#根据年月来对文章进行分类
# def y_m_count(timeset):
#     a = []
#     print(timeset)
#     for i in timeset:
#         print(i)
#         year = i[0].year
#         month = i[0].month
#         a.append((year, month))
#
#     y_m_dicts = {}
#     for i in a:
#         y_m_dicts.setdefault(i, a.count(i))
#
#     return y_m_dicts

#个人首页展示
def homeSite(request,username,**kwargs):
    print(username)
    print(kwargs)
    user=models.Userinfo.objects.filter(username=username).first()
    if not user:
        return render(request, 'notFound.html')
    else:
        from django.db.models import Count
        date_list = models.Article.objects.filter(user=user).extra(
            select={"filter_create_date": "strftime('%%Y/%%m',create_time)"}).values_list(
            "filter_create_date").annotate(c=Count("id"))
        if kwargs:
            if kwargs.get("condition")=="tag":
                articles=models.Article.objects.filter(tags__title=kwargs.get("para"),user__username=username)
            elif kwargs.get("condition")=="category":
                articles = models.Article.objects.filter(category__title=kwargs.get("para"),user__username=username)
            elif kwargs.get("condition")=="date":
                year,month=kwargs.get('para').split("/")
                articles=models.Article.objects.filter(create_time__year=year,create_time__month=month,user__username=username)


        else:
            articles = models.Article.objects.filter(user=user).all()

        print(articles)
        return render(request,"homeSite.html",{"user":user,"articles":articles,"date_list":date_list})


        #     if user:
        #         article_categroy=kwargs.get("article_categroy")
        #         article_tag=kwargs.get("article_tag")
        #         year=kwargs.get("year")
        #         print(type(year),"*****************-")
        #         month=kwargs.get("month")
        #         if article_categroy:
        #             articles=models.Article.objects.filter(category__title=article_categroy).all()
        #         elif article_tag:
        #             articles=models.Article.objects.filter(tags__title=article_tag).all()
        #         elif month and year:
        #             article_set = models.Article.objects.filter(user=user).all()
        #             articles=[]
        #             for article in article_set:
        #                 print(type(article.create_time.year))
        #                 if str(article.create_time.year)==year and str(article.create_time.month)==month:
        #                     articles.append(article)
        #             print(articles)
        #         else:
        #             articles=models.Article.objects.filter(user=user).all()
        #         timeset=models.Article.objects.filter(user=user).values_list("create_time")
        #         y_m_dicts=y_m_count(timeset)
        #         return render(request,'homeSite.html',{"user":user,"articles":articles,"y_m_dicts":y_m_dicts})
        #     else:
        #         return render(request,'notFound.html')

#文章详细处理
def articleDetail(request,username,article_id):
    print(username)
    user = models.Userinfo.objects.filter(username=username).first()
    print(user)
    from django.db.models import Count
    date_list = models.Article.objects.filter(user=user).extra(
        select={"filter_create_date": "strftime('%%Y/%%m',create_time)"}).values_list(
        "filter_create_date").annotate(c=Count("id"))

    article=models.Article.objects.filter(id=article_id).first()
    models.Article.objects.filter(id=article_id).update(read_count=F('read_count')+1)
    print(article)
    return render(request,"article.html",{'articleobj':article,"user":user,"date_list":date_list})

#点赞
def articleDiggit(request):
    article_id=request.POST.get("article_id")
    user_id=request.user.id
    diggit_response={"flag":False,"errors":None}
    if models.ArticleUp.objects.filter(user_id=user_id,article_id=article_id):
        diggit_response["errors"]="不能重复点赞"
    else:
        try:
            diggit_response['flag']=True
            models.ArticleUp.objects.create(user_id=user_id,article_id=article_id)

            models.Article.objects.filter(id=article_id).update(up_count=F("up_count")+1)
        except:
            diggit_response["errors"]="未知错误"
    return  HttpResponse(json.dumps(diggit_response))

#文章反对
def articleBuryit(request):
    article_id = request.POST.get("article_id")
    user_id = request.user.id
    buryit_response={"flag":False,"errors":None}
    if models.ArticleDown.objects.filter(user_id=user_id,article_id=article_id):
        buryit_response["errors"]="不能重复反对"
    else:
        try:
            models.ArticleDown.objects.create(article_id=article_id,user_id=user_id)
            models.Article.objects.update(down_count=F("down_count")+1)
            buryit_response["flag"]=True
        except:
            buryit_response["errors"]="未知错误"
    return HttpResponse(json.dumps(buryit_response))



#文章评论
def articleComment(request):
    if request.user.is_authenticated():
        article_id = request.POST.get("article_id")
        user_id = request.user.id
        content=request.POST.get("content")
        comment_response={"flag":True,"errors":None,"comment_time":None}
        try:
            comment=models.Comment.objects.create(article_id=article_id,user_id=user_id,content=content)
            models.Article.objects.filter(id=article_id).update(comment_count=F("comment_count")+1)

            time=models.Comment.objects.filter(id=comment.id).extra(select={"comment_time":"strftime('%%Y-%%m-%%d %%H:%%M:%%S',create_time)"}).values_list("comment_time")
            comment_response["comment_time"]=time[0][0]
        except:
            comment_response["flag"]=False
            comment_response["errors"]="未知错误"
        return HttpResponse(json.dumps(comment_response))
    else:
        return redirect("/login/")



