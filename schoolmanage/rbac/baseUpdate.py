
class BasePagePermission(object):
    def __init__(self,code_list):
        self.code_list=code_list
    def has_add(self):
        if "add" in self.code_list:
            return True

    def has_edit(self):
        if "edit" in self.code_list:
            return True
    def has_del(self):
        if "del" in self.code_list:
            return  True

