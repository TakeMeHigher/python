from django.conf import settings
from django.shortcuts import redirect
import re
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

class Middleware(MiddlewareMixin):
    def process_request(self, request):
        current_url=request.path_info
        print(current_url)
        # for url in settings.VALID_URL:
        #     print(url)
        #     if re.match(url,current_url):
        #         return None
        #     return redirect("/login/")
        if request.user.is_authenticated():
            return None


        for url in settings.VALID_URL:
            if re.match(url,current_url):
                return None

        else:
            return redirect("/login/")



