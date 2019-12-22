from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta



from .models import *



    
class ExternalLinkAdmin(admin.ModelAdmin):
    
    def count(self, obj):
        return obj.access.count()
    count.short_description = "Total Access"
    
    def month_count(self, obj):
        last_month = timezone.now() - timedelta(days=30)
        return obj.access.filter(timestamp__gte=last_month).count()
    month_count.short_description = "Last Month Access"
    
    
    def requests(self, obj):
        url = "/admin/request/request/?path=/link/{}/".format(obj.name)
        link = format_html("<a href='{url}'>requests</a>", url=url)
        return link
    requests.short_description = 'requests'
    
    list_display = ('__str__', 'url', 'count', 'month_count', 'requests')
    
    
class LinkAccessAdmin(admin.ModelAdmin):
    list_display = ('link', 'timestamp', )








def mark_read(modeladmin, request, queryset):
    queryset.update(read=True)
mark_read.short_description = "Mark selected messages as read"


class MessageAdmin(admin.ModelAdmin):
    def date(self, obj):
        return str(obj.created.date())
    
    list_display = ('date', 'read', 'name', 'message')
    actions = [mark_read]


admin.site.register(LinkAccess, LinkAccessAdmin)
admin.site.register(ExternalLink, ExternalLinkAdmin)
admin.site.register(Message, MessageAdmin)
