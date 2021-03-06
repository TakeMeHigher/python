from django.db import models

# Create your models here.

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    publishDate = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    publish=models.ForeignKey("Publish")
    authors=models.ManyToManyField("Author")

    def __str__(self):
        return self.title

class Publish(models.Model):
    name=models.CharField(max_length=32)
    addr=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Author(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()
    addr=models.CharField(max_length=120)
    phone=models.CharField(max_length=32)

    def __str__(self):
        return self.name




