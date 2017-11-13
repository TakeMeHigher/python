from django.db import models

class Menu(models.Model):
    title=models.CharField(max_length=32,verbose_name="菜单名称")

class group(models.Model):
    '''
    用户组表
    '''
    caption=models.CharField(max_length=32)
    menu=models.ForeignKey(verbose_name="所属菜单",to="Menu",default=1)

class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题',max_length=32)
    url = models.CharField(verbose_name="含正则URL",max_length=64)
    #is_menu = models.BooleanField(verbose_name="是否是菜单")
    menu_gp=models.ForeignKey(verbose_name="组内菜单",to="Permission",null=True,blank=True)
    code=models.CharField(max_length=32,verbose_name="代码",null=True)
    group=models.ForeignKey(verbose_name="所在分组",to="Group",null=True)
    class Meta:
        verbose_name_plural = "权限表"

    def __str__(self):
        return self.title

class User(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name='用户名',max_length=32)
    password = models.CharField(verbose_name='密码',max_length=64)
    email = models.CharField(verbose_name='邮箱',max_length=32)

    roles = models.ManyToManyField(verbose_name='具有的所有角色',to="Role",blank=True)
    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.username

class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(verbose_name='具有的所有权限',to='Permission',blank=True)
    class Meta:
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.title






