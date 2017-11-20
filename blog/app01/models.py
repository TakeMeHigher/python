from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Userinfo(AbstractUser):
    '''
    用户表
    '''
    id=models.BigAutoField(primary_key=True)

    nickname=models.CharField(max_length=32,verbose_name="昵称")
    phone = models.CharField(max_length=11,blank=True,null=True,unique=True, verbose_name="电话")
    avatar = models.FileField(verbose_name='头像', upload_to='avatar', default="/avatar/default.png")
    registTime = models.DateTimeField(verbose_name="注册时间",auto_now_add=True)

class Blog(models.Model):
    '''
    博客表
    '''
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)

    user = models.OneToOneField(to='UserInfo', to_field='id')

    def __str__(self):
        return self.title

class Category(models.Model):
    """
    博主个人文章分类表
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='id')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'category'
        ordering = ['title']

class Article(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='id', null=True)
    user = models.ForeignKey(verbose_name='所属用户', to='Userinfo', to_field='id')
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    type_choices = [
        (1, "编程语言"),
        (2, "软件设计"),
        (3, "前端"),
        (4, "操作系统"),
        (5, "数据库"),
    ]

    article_type_id = models.IntegerField(choices=type_choices, default=None)

    def __str__(self):
        return self.title

class ArticleDetail(models.Model):
    """
    文章详细表
    """
    id = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容', )

    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='id')

class Comment(models.Model):
    """
    评论表
    """
    id = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    up_count = models.IntegerField(default=0)

    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='id')
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='id')

    parent_comment = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    def __str__(self):
        return self.content

class CommentUp(models.Model):
    """
    评论点赞表
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    comment = models.ForeignKey("Comment", null=True)

class ArticleUp(models.Model):
    """
    点赞表
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    article = models.ForeignKey("Article", null=True)

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='id')

class Article2Tag(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='id')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='id')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]


