from django.db import models

# Create your models here.
class ClassList(models.Model):
    """
    班级表
    """
    caption = models.CharField(max_length=32)
    headmaster = models.ForeignKey(to="UserInfo")

class Student(models.Model):
    """
    学生表
    """
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    sex_choice = (("m","男"), ("f", "女"),)
    sex= models.CharField(max_length=10, choices=sex_choice)
    email=models.EmailField(default="aa@qq.com")
    cls = models.ForeignKey(to="ClassList")

class UserType(models.Model):
    """
    用户类型表,个数经常变动
    """
    title = models.CharField(max_length=32)

class UserInfo(models.Model):
    """
    用户表：讲师和班主任
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=32)
    age=models.IntegerField(default=21)
    sex_choice = (("m","男"), ("f", "女"),)
    sex = models.CharField(max_length=10, choices=sex_choice)

    ut = models.ForeignKey(to="UserType")
    teacher_to_cls = models.ManyToManyField(to='ClassList')

# ###############################################