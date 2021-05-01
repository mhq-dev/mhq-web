from django.contrib import admin

from request import models

admin.site.register(models.Request)
admin.site.register(models.KeyValueContainer)
