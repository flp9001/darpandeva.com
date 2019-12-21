from django.contrib import admin

from .models import *


class LinkAccessAdmin(admin.ModelAdmin):
    list_display = ('url', 'timestamp')

admin.site.register(LinkAccess, LinkAccessAdmin)
