from django.test import TestCase

# Create your tests here.
# info_dic={}
# d=info_dic.fromkeys(('name','age','sex'),None)
# print(d)
d1=dict.fromkeys(('name','age','sex'),None)
d2=dict.fromkeys(('name','age','sex'),('egon',18,'male'))
print(d1)
print(d2)


# info_dic={'name':'egon','age':18,'sex':'male'}
# info_dic.update({'a':1,'name':'Egon'})
# print(info_dic)

# l=['a','b','c','d','e','f']
#
# print(l[1:5])
# print(l[1:5:2])
# print(l[2:5])
# print(l[-1])
#
#
# #了解

info=dict(name='egon',age=18,sex='male')
print(info)


info=dict([('name','egon'),('age',18)])
print(info)