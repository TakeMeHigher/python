from django.conf import settings
def init_permission(request,user):
    permission_list = user.roles.values(
        "permissions__title",
        "permissions__id",
        "permissions__url",
        "permissions__code",
        "permissions__menu_gp_id",
        "permissions__group_id",
        "permissions__group__menu_id",
        "permissions__group__menu__title",
         ).distinct()


    menu_list=[]
    for item in permission_list:
        tpl={
            "id":item["permissions__id"],
            "title":item["permissions__title"],
            "url":item["permissions__url"],
            "menu_title":item["permissions__group__menu__title"],
            "menu_id":item["permissions__group__menu_id"],
            "menu_gp":item["permissions__menu_gp_id"],
        }
        menu_list.append(tpl)
    request.session[settings.PERMISSIONS_MENU_KEY] = menu_list
    # menu_list=[]
    # for item in permission_list:
    #     menu_id=item["permissions__group__menu_id"]
    #     menu_title=item["permissions__group__menu__title"]
    #     title=item["permissions__title"]
    #     url=item["permissions__url"]
    #     if not item["permissions__is_menu"]:
    #         continue
    #     tpl={
    #         "menu_id":menu_id,
    #         "menu_title":menu_title,
    #         "title":title,
    #         "url":url,
    #         "active":False,
    #     }
    #     menu_list.append(tpl)
    # print(menu_list)

    # request.session[settings.PERMISSIONS_MENU_KEY]=menu_list
   #3权限操作



    res={}
    for item in permission_list:
        group_id=item["permissions__group_id"]
        url=item["permissions__url"]
        code=item["permissions__code"]

        if group_id in res:
            res[group_id]["codes"].append(code)
            res[group_id]["url"].append(url)
        else:
            res[group_id]={
                "codes":[code,],
                "url":[url,]
            }
    request.session[settings.PERMISSSION_URL_LIST] = res
    request.session["userinfo"]={"username":user.username,"password":user.password,"id":user.id}

