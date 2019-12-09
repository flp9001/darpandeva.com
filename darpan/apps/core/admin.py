from django.contrib import admin
from django.utils.html import format_html
from .models import *



def mark_read(modeladmin, request, queryset):
    queryset.update(read=True)
mark_read.short_description = "Mark selected messages as read"

class MessageAdmin(admin.ModelAdmin):
    def change_url(self, obj):
        if not obj.read:
            return format_html('<strong>Unread</strong>')
        return format_html('Read')
        
    
    
    list_display = ('created', 'change_url', 'name', 'phone', 'email', 'message')
    actions = [mark_read]
    

admin.site.register(Message, MessageAdmin)
