from django.test import TestCase

# Create your tests here.
# info_dic={}
# d=info_dic.fromkeys(('name','age','sex'),None)
# print(d)
# d1=dict.fromkeys(('name','age','sex'),None)
# d2=dict.fromkeys(('name','age','sex'),('egon',18,'male'))
# print(d1)
# print(d2)


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
#
# info=dict(name='egon',age=18,sex='male')
# print(info)
#
#
# info=dict([('name','egon'),('age',18)])
# print(info)


#原始版
'''
comment_list = [
    {"id": 1, "content": "...", "Pid": None},
    {"id": 2, "content": "...", "Pid": None},
    {"id": 3, "content": "...", "Pid": None},
    {"id": 4, "content": "...", "Pid": 1},
    {"id": 5, "content": "...", "Pid": 1},
    {"id": 6, "content": "...", "Pid": 4},
    {"id": 7, "content": "...", "Pid": 3},
    {"id": 8, "content": "...", "Pid": 7},
    {"id": 9, "content": "...", "Pid": None},

]

for i in comment_list:
    i["children_comment"] = []


'''
'''
[
 {'id': 1, 'content': '...', 'Pid': None, 'children_comment': []},
 {'id': 2, 'content': '...', 'Pid': None, 'children_comment': []}, 
 {'id': 3, 'content': '...', 'Pid': None, 'children_comment': []}, 
 {'id': 4, 'content': '...', 'Pid': 1, 'children_comment': []}, 
 {'id': 5, 'content': '...', 'Pid': 1, 'children_comment': []}, 
 {'id': 6, 'content': '...', 'Pid': 4, 'children_comment': []},
 {'id': 7, 'content': '...', 'Pid': 3, 'children_comment': []}, 
 {'id': 8, 'content': '...', 'Pid': 7, 'children_comment': []},
 {'id': 9, 'content': '...', 'Pid': None, 'children_comment': []}
   ]
'''
'''

for j in comment_list:
    if j["Pid"]:
        pid = j["Pid"]
        for x in comment_list:
           if x["id"]==pid:
               x["children_comment"].append(j)

print(comment_list)






l = []
for a in comment_list:
    if not a["Pid"]:
        l.append(a)

print(l)
'''



comment_list = [
    {"id": 1, "content": "...", "Pid": None},
    {"id": 2, "content": "...", "Pid": None},
    {"id": 3, "content": "...", "Pid": None},
    {"id": 4, "content": "...", "Pid": 1},
    {"id": 5, "content": "...", "Pid": 1},
    {"id": 6, "content": "...", "Pid": 4},
    {"id": 7, "content": "...", "Pid": 3},
    {"id": 8, "content": "...", "Pid": 7},
    {"id": 9, "content": "...", "Pid": None},

]

count=1
comment_dic={}
for comment in comment_list:
    comment["children_comment"]=[]
    comment_dic[count]=comment
    count+=1
#print(comment_dic)

'''
{
1: 
    {'id': 1, 'content': '...', 'Pid': None, 'children_comment': []}, 
2: 
    {'id': 2, 'content': '...', 'Pid': None, 'children_comment': []},
3: 
    {'id': 3, 'content': '...', 'Pid': None, 'children_comment': []}, 
4: 
    {'id': 4, 'content': '...', 'Pid': 1, 'children_comment': []}, 
5: 
    {'id': 5, 'content': '...', 'Pid': 1, 'children_comment': []}, 
6: 
    {'id': 6, 'content': '...', 'Pid': 4, 'children_comment': []}, 
7: 
    {'id': 7, 'content': '...', 'Pid': 3, 'children_comment': []}, 
8: 
    {'id': 8, 'content': '...', 'Pid': 7, 'children_comment': []}, 
9: 
    {'id': 9, 'content': '...', 'Pid': None, 'children_comment': []}
 }
'''

for i in comment_dic:
    for j in comment_dic:
        if comment_dic[i]["id"] == comment_dic[j]["Pid"]:
            comment_dic[i]["children_comment"].append(comment_dic[j])
dic={}
for a in comment_dic:
    if not comment_dic[a]["Pid"]:
        dic[a]=comment_dic[a]

print(dic)

'''
{
 1: 
   {'id': 1, 'content': '...', 'Pid': None, 
      'children_comment': [
           {'id': 4, 'content': '...', 'Pid': 1, 
                 'children_comment': [
                    {'id': 6, 'content': '...', 'Pid': 4, 'children_comment': []}]}, 
                    {'id': 5, 'content': '...', 'Pid': 1, 'children_comment': []}]}, 
 2: 
   {'id': 2, 'content': '...', 'Pid': None, 'children_comment': []}, 
 3:
   {'id': 3, 'content': '...', 'Pid': None, 
       'children_comment': [
           {'id': 7, 'content': '...', 'Pid': 3, 
               'children_comment': [
                   {'id': 8, 'content': '...', 'Pid': 7, 'children_comment': []}]}]}, 
9: {'id': 9, 'content': '...', 'Pid': None, 'children_comment': []}}

'''

