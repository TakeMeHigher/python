from django.db import models

# Create your models here.
class ClassList(models.Model):
    """
    班级表
    """
    caption = models.CharField(verbose_name="班级名称",max_length=32)
    headmaster = models.ForeignKey(verbose_name="班主任",to="UserInfo")

    class Meta:
        verbose_name_plural="班级表"

class Student(models.Model):
    """
    学生表
    """
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    sex_choice = (("m","男"), ("f", "女"),)
    sex= models.CharField(max_length=10, choices=sex_choice)
    email=models.EmailField(default="aa@qq.com")
    cls = models.ForeignKey(verbose_name="所在班级",to="ClassList")

    class Meta:
        verbose_name_plural="学生表"

class UserType(models.Model):
    """
    用户类型表,个数经常变动
    """
    title = models.CharField(max_length=32)
    class Meta:
        verbose_name_plural="用户类型表"


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
    ut = models.ForeignKey(verbose_name="用户类型",to="UserType")
    teacher_to_cls = models.ManyToManyField(verbose_name="老师所交班级",to='ClassList')


    class Meta:
        verbose_name_plural="用户表"

# ###############################################