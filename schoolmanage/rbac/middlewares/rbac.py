import  re
from django.conf import settings
from django.shortcuts import render,redirect,HttpResponse
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class RbacMiddleware(MiddlewareMixin):
    def process_request(self,request):
        #获取当前访问的路径
        currentPath=request.path_info

        #白名单
        VALID_URL=settings.VALID_URL

        for url in VALID_URL:
            if re.match(url,currentPath):
                return None

        permission_url_list=request.session.get(settings.PERMISSSION_URL_LIST)
        if not permission_url_list:
            return redirect("/login/")
        flag=False
        for k,code_url in permission_url_list.items():
            for db_url in code_url["url"]:
                regex="^{0}$".format(db_url)
                if re.match(regex,currentPath):
                    request.permission_code_list=code_url["codes"]
                    flag=True
                    break
            if flag:
                break

        if not flag:
            return HttpResponse("无权访问")






