from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from app01 import models
from app01.forms import RegForm
import json
import random

# Create your views here.
#登录
def login(request):
    if request.method=="POST":
        name = request.POST.get("name")
        pwd = request.POST.get("pwd")
        valid_Code=request.POST.get('valid_Code')
        print(valid_Code)
        login_dic = {"is_login": False,"msg":None}
        if valid_Code.upper()==request.session.get('valid_str').upper():
            user = models.Userinfo.objects.filter(username=name, password=pwd).first()
            # user=auth.authenticate(username=name,password=pwd)
            print(name,pwd)
            if user:
                request.session['userinfo']={"username":name,'id':user.id}
                auth.login(request,user)
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
       print(type(form))
       if form.is_valid():
           # print(form.cleaned_data)
           # print(form.cleaned_data.get('avatar'))
           confirmPassword=form.cleaned_data.pop('confirmPassword')
           models.Userinfo.objects.create(**form.cleaned_data)
           return redirect('/login/')
       return  render(request,'reg.html',{'form':form})

    form=RegForm()
    return render(request,'reg.html',{'form':form})

#首页
def index(request):
    if request.session.get('userinfo'):
        return render(request,'index.html')
    return redirect('/login/')

#注销
def logout(request):
    request.session.flush()
    return redirect('/login/')





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


