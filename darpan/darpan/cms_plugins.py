from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .forms import ContactForm

@plugin_pool.register_plugin
class ContactPlugin(CMSPluginBase):
    model = CMSPlugin
    name = "Form: Contact"
    render_template = "contact_form/contact_plugin.html"

    def render(self, context, instance, placeholder):
        request = context['request']
        context.update({
            'instance': instance,
            'placeholder': placeholder,
            'form': ContactForm,
        })
        return context


