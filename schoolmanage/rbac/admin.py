from django.contrib import admin

from . import models


admin.site.register(models.Permission)
admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.group)
admin.site.register(models.Menu)
