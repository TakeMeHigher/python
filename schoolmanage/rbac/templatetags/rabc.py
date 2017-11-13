import re
from django.template import Library
from django.conf import  settings

register=Library()

@register.inclusion_tag("test.html")
def menu_html(request):
    currentPath=request.path_info
    menu_list=request.session.get(settings.PERMISSIONS_MENU_KEY)
    print(currentPath)
    print(menu_list)

    menu_dict={}
    for item in menu_list:
        if not item["menu_gp"]:
            print(item)
            menu_dict[item["id"]]=item
    for item in menu_list:
        url=item["url"]
        regex="^{0}$".format(url)
        if re.match(regex,currentPath):
            menu_gp=item['menu_gp']
            if not menu_gp:
                menu_dict[item["id"]]["active"]=True
            else:
                menu_dict[menu_gp]["active"]=True
    print(menu_dict)
    res={}

    for item in menu_dict.values():
        active=item.get("active")
        if item["menu_id"] in res:
            res[item["menu_id"]]["children"].append({"title":item["title"],"url":item["url"],"active":active})
            if active:
                res[item["menu_id"]]["active"]=True
        else:
            res[item["menu_id"]]={
                "menu_id":item["menu_id"],
                "menu_title":item["menu_title"],
                "active":active,
                "children":[
                    {"title":item["title"],"url":item["url"],"active":active},
                ]

            }
    print(res)


    #
    # for item in menu_list:
    #     menu_title=item["menu_title"]
    #     menu_id=item["menu_id"]
    #     title=item["title"]
    #     url=item["url"]
    #     active=False
    #
    #     regex="^{0}$".format(url)
    #     if re.match(regex,currentPath):
    #         active=True
    #
    #     if menu_id in res:
    #         res[menu_id]["children"].append({"title":title,"url":url,"active":active},)
    #         if active:
    #             res[menu_id]["active"]=True
    #     else:
    #         res[menu_id]={
    #             "menu_id":menu_id,
    #             "menu_title":menu_title,
    #             "active":active,
    #             "children":[
    #                 {"title":title,"url":url,"active":active},
    #             ]
    #
    #         }
    print(res)
    return {"menu_list":res}