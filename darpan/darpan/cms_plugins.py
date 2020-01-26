from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .forms import ContactForm
from djangocms_picture.models import AbstractPicture

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



class LazyPicture(AbstractPicture):
    external_picture = models.CharField(
        verbose_name=_('External image'),
        blank=True,
        null=True,
        max_length=32*1024,
        help_text=_(
            'If provided, overrides the embedded image. '
            'Certain options such as cropping are not applicable to external images.'
        )
    )
    
    
    class Meta:
        abstract = False



@plugin_pool.register_plugin
class LazyPicturePlugin(CMSPluginBase):
    model = LazyPicture
    name = "Lazy Picture"
    
    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_picture/{}/picture.html'.format(instance.template)

    def render(self, context, instance, placeholder):
        if instance.alignment:
            classes = 'align-{} '.format(instance.alignment)
            classes += instance.attributes.get('class', '')
            # Set the class attribute to include the alignment html class
            # This is done to leverage the attributes_str property
            instance.attributes['class'] = classes
        # assign link to a context variable to be performant
        context['picture_link'] = instance.get_link()
        context['picture_size'] = instance.get_size(
            width=context.get('width') or 0,
            height=context.get('height') or 0,
        )
        context['img_srcset_data'] = instance.img_srcset_data

        return super(LazyPicturePlugin, self).render(context, instance, placeholder)
