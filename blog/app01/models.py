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

    class Meta:
        verbose_name_plural="用户表"

    def __str__(self):
        return self.username

class Blog(models.Model):
    '''
    博客表
    '''
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)

    user = models.OneToOneField(to='Userinfo', to_field='id')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="博客表"

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
        verbose_name_plural = '文章分类表'
        ordering = ['title']

class Article(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    read_count = models.IntegerField(default=0,verbose_name='阅读数')
    comment_count = models.IntegerField(default=0,verbose_name="评论数")
    up_count = models.IntegerField(default=0,verbose_name="点赞数")
    down_count = models.IntegerField(default=0,verbose_name="差评数")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='id', null=True)
    user = models.ForeignKey(verbose_name='所属用户', to='Userinfo', to_field='id')
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    siteArticleCategory=models.ForeignKey(to="SiteArticleCategory",verbose_name="所属网站文章分类",null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="文章表"

class ArticleDetail(models.Model):
    """
    文章详细表
    """
    id = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容', )

    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='id')

    class Meta:
        verbose_name_plural="文章详细表"

    def __str__(self):
        return self.article.title

class Comment(models.Model):
    """
    评论表
    """
    id = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    up_count = models.IntegerField(default=0)

    user = models.ForeignKey(verbose_name='评论者', to='Userinfo', to_field='id')
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='id')

    parent_comment = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural="评论表"

class CommentUp(models.Model):
    """
    评论点赞表
    """

    id = models.AutoField(primary_key=True,verbose_name='评论点赞id')
    user = models.ForeignKey('Userinfo', null=True,verbose_name="点赞人")
    comment = models.ForeignKey("Comment", null=True,verbose_name="点赞的评论")

    class Meta:
        verbose_name_plural='评论点赞表'




class ArticleUp(models.Model):
    """
    文章点赞表
    """
    id = models.AutoField(primary_key=True,verbose_name='文章点赞id')
    user = models.ForeignKey('Userinfo', null=True,verbose_name='点赞人')
    article = models.ForeignKey("Article", null=True,verbose_name="点赞的文章")

    class Meta:
        verbose_name_plural="文章点赞表"

class ArticleDown(models.Model):
    """
    文章反对表
    """
    id = models.AutoField(primary_key=True,verbose_name='文章反对id')
    user = models.ForeignKey('Userinfo', null=True,verbose_name='反对人')
    article = models.ForeignKey("Article", null=True,verbose_name="反对的文章")

    class Meta:
        verbose_name_plural="文章反对表"

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='id')

    class Meta:
        verbose_name_plural="标签表"

    def __str__(self):
        return  self.title

class Article2Tag(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='id')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='id')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

        verbose_name_plural='文章和标签关联表'

class SiteCategory(models.Model):
    '''
    网站分类
    '''
    name=models.CharField(max_length=32,verbose_name='网站分类名称')
    class Meta:
        verbose_name_plural='网站分类表'

    def __str__(self):
        return self.name


class SiteArticleCategory(models.Model):
    '''
    网站分类对应的文章分类表
    '''
    name=models.CharField(max_length=32,verbose_name="网站文章分类名称")

    siteCategory=models.ForeignKey(to="SiteCategory",verbose_name='所属网站分类')

    class Meta:
        verbose_name_plural='网站文章分类表'

    def __str__(self):
        return self.name