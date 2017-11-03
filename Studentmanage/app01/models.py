from django.db import models

# Create your models here.

class Student(models.Model):
    sname=models.CharField(max_length=32)
    age=models.IntegerField()
    sex_choice=(("male","男"),("female","女"))
    sex=models.CharField(max_length=10,choices=sex_choice)
    email=models.CharField(max_length=32)
    addr=models.CharField(max_length=32)
    phone=models.CharField(max_length=32)
    #学生和班主任 m2o
    headmaster=models.ForeignKey("Headmaster")
    #学生和班级 m2o
    classes=models.ForeignKey("Class")
    




class Class(models.Model):
    cname=models.CharField(max_length=32)

    #班级和班主任 m2o
    headmaster = models.ForeignKey("Headmaster")
    #班级和老师 m2m
    teachers=models.ManyToManyField("Teacher")

class Teacher(models.Model):
    tname=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    age = models.IntegerField()
    sal=models.DecimalField(max_digits=7,decimal_places=2)
    sex_choice = (("male", "男"), ("female", "女"))
    sex = models.CharField(max_length=10, choices=sex_choice)
    email = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)


class Headmaster(models.Model):
    hname=models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    age = models.IntegerField()
    sal = models.DecimalField(max_digits=7, decimal_places=2)
    sex_choice = (("male", "男"), ("female", "女"))
    sex = models.CharField(max_length=10, choices=sex_choice)
    email = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)


