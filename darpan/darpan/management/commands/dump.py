from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.management import call_command
from django.core.management.commands import loaddata, dumpdata


APPS = [
    "cms",
    "darpan",
    "sites",
    "bootstrap4_alerts",
    "bootstrap4_badge",
    "bootstrap4_card",
    "bootstrap4_carousel",
    "bootstrap4_collapse",
    "bootstrap4_content",
    "bootstrap4_grid",
    "bootstrap4_jumbotron",
    "bootstrap4_link",
    "bootstrap4_listgroup",
    "bootstrap4_media",
    "bootstrap4_picture",
    "bootstrap4_tabs",
    "bootstrap4_utilities",
    "djangocms_googlemap",
    "djangocms_icon",
    "djangocms_link",
    "djangocms_picture",
    "djangocms_snippet",
    "djangocms_style",
    "djangocms_text_ckeditor",
    "djangocms_video",
    "easy_thumbnails",
    "filer",
    "menus",
    "request",
]


class Command(BaseCommand):
    help = 'Dump CMS Data'
    
    def handle(self, *args, **options):
        call_command('dumpdata', '--natural-foreign', '--indent 2', *APPS)
        
