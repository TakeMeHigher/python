# from django.shortcuts import render,HttpResponse
# from . import models
# # Create your views here.
#
# def test(request):
#     name="番禺"
#     pwd="123"
#
#     user=models.User.objects.filter(username=name,password=pwd).first()
#     if user:
#         print(user.roles.all().values("title"))
#         priviliges=models.User.objects.filter(username=name, password=pwd).values_list("roles__title","roles__permissions__title").distinct()
#         return render(request,"test.html",{"priviliges":priviliges})
#     else:
#         return HttpResponse("用户名或密码不正确")


