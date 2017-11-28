from django import forms
from django.forms import fields,widgets
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from app01 import models
class RegForm(forms.Form):
    username = forms.CharField(required=True, min_length=3,
                               error_messages={"required": '用户名不能为空','min_length':'用户名长度最小为3'},
                               widget=forms.widgets.TextInput(
                                   attrs={"class": "form-control", 'placeholder': '登录用户名，不少于3个字符', 'id': "username"})
                               )
    nickname = forms.CharField(required=True, min_length=2,max_length=20,
                               error_messages={"required": '昵称不能为空',"min_length":'昵称最小长度为2','max_length':'昵称最大长度为20'},
                               widget=forms.widgets.TextInput(
                                   attrs={"class": "form-control", 'placeholder': '即昵称，不少于2个字符', 'id': "nickname"})
                               )
    email = forms.EmailField(required=True, error_messages={"required": '邮箱不能为空'},
                             widget=forms.widgets.TextInput(
                                 attrs={"class": "form-control", 'placeholder': '邮箱', 'id': "email"})
                             )

    phone = forms.CharField(required=True, error_messages={"required": '手机号码不能为空'},
                             widget=forms.widgets.TextInput(
                                 attrs={"class": "form-control", 'placeholder': '手机号码', 'id': "phone"})
                             )
    password = forms.CharField(required=True, min_length=8,
                               error_messages={"required": '密码不能为空','min_length':'密码最小长度为8'},
                               validators=[
                                   RegexValidator(r'((?=.*\d))^.{8,}$', '必须包含数字'),
                                   RegexValidator(r'((?=.*[a-zA-Z]))^.{8,}$', '必须包含字母'),
                               ],
                             widget=forms.widgets.TextInput(
                                 attrs={"class": "form-control", 'placeholder': '至少8位，必须包含字母、数字', 'id': "password"}

                             )
                             )
    confirmPassword = forms.CharField(required=True, error_messages={"required": '确认密码不为空'},
                                widget=forms.widgets.TextInput(
                                    attrs={"class": "form-control", 'placeholder': '请输入确认密码', 'id': "confirmPassword"})
                                )
    # avatar=forms.FileField(required=True,error_messages={'required':'头像不能为空'})

    def clean_username(self):
        user=models.Userinfo.objects.filter(username=self.cleaned_data.get("username")).first()
        if user:
            raise ValidationError('用户名已经被注册')

        else:
            return self.cleaned_data.get('username')


    def clean_email(self):

        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',self.cleaned_data.get("email")):
            return self.cleaned_data.get('email')
        else:
            raise ValidationError('邮箱格式不正确')

    def clean_phone(self):
        pattern=re.compile('^1[3458]\d{9}$')
        if pattern.match(self.cleaned_data.get('phone')):
            return self.cleaned_data.get('phone')
        else:
            raise ValidationError('手机号码格式不正确')

    def clean_confirmPassword(self):
        confirmPassword=self.cleaned_data.get('confirmPassword')
        password=self.cleaned_data.get('password')
        if confirmPassword==password:
            return self.cleaned_data.get('confirmPassword')
        else:
            raise ValidationError('确认密码输入错误')


class ArticleForm(forms.Form):
    title=fields.CharField(max_length=30,error_messages={"required":"标题不能为空"},
                          widget=widgets.TextInput(attrs={"id":"tilte","style":"width:800px"})
                          )

    content=fields.CharField(error_messages={"required":"内容不能为空"},
                             widget=widgets.Textarea(attrs={"id":"article_content"})
                             )


    category_id=fields.ChoiceField(choices=[],widget=widgets.RadioSelect(attrs={"class":"list-unstyled list-inline"}))

    tag_ids=fields.MultipleChoiceField(choices=[],widget=widgets.CheckboxSelectMultiple(attrs={"class":"list-unstyled list-inline"}))

    siteArticleCategory_id=fields.ChoiceField(choices=[],widget=widgets.RadioSelect(attrs={"class":"list-unstyled list-inline"}))



    def __init__(self,user_id,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["category_id"].choices=models.Category.objects.filter(blog__user_id=user_id).values_list("id","title")
        self.fields["tag_ids"].choices=models.Tag.objects.filter(blog__user_id=user_id).values_list("id","title")
        self.fields["siteArticleCategory_id"].choices=models.SiteArticleCategory.objects.all().values_list("id","name")