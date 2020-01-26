from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .forms import ContactForm

from djangocms_picture.models import AbstractPicture
from filer.fields.image import FilerImageField
from filer.models import ThumbnailOption
from easy_thumbnails.files import get_thumbnailer
from djangocms_attributes_field.fields import AttributesField

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
    self_link = models.BooleanField(
        verbose_name=_('Wraps with a link to the original image'),
        default=False,
        blank=True,
        null=True,
        )
    placeholder_picture = FilerImageField(
        verbose_name=_('Placeholder Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    
    placeholder_thumbnail_options = models.ForeignKey(
        ThumbnailOption,
        verbose_name=_('Placeholder Thumbnail options'),
        blank=True,
        null=True,
        help_text=_('Overrides width, height, and crop; scales up to the provided preset dimensions.'),
        on_delete=models.CASCADE,
        related_name = 'placeholder_thumbnail_options'
    )
    
    placeholder_base64_picture = models.CharField(
        verbose_name=_('Placeholder Base64 image'),
        blank=True,
        null=True,
        max_length=32*1024,
        help_text=_(
            'If provided, overrides the embedded image. '
            'Certain options such as cropping are not applicable to external images.'
        )
    )
    
    span_attributes = AttributesField(
        verbose_name=_('Span attributes'),
        blank=True,
        excluded_keys=['href', 'target'],
    )
    
    def get_link(self):
        if self.self_link:
            return self.picture.url
        if self.external_picture:
            return self.external_picture
        elif self.link_url:
            return self.link_url
        elif self.link_page_id:
            return self.link_page.get_absolute_url(language=self.language)
        return False
        
    def get_placeholder_size(self, width=None, height=None):
        crop = self.use_crop
        upscale = self.use_upscale
        # use field thumbnail settings
        if self.placeholder_thumbnail_options:
            width = self.placeholder_thumbnail_options.width
            height = self.placeholder_thumbnail_options.height
            crop = self.placeholder_thumbnail_options.crop
            upscale = self.placeholder_thumbnail_options.upscale
        elif not self.use_automatic_scaling:
            width = self.width
            height = self.height

        # calculate height when not given according to the
        # golden ratio or fallback to the picture size
        if not height and width:
            height = int(width / PICTURE_RATIO)
        elif not width and height:
            width = int(height * PICTURE_RATIO)
        elif not width and not height and self.picture:
            width = self.picture.width
            height = self.picture.height

        options = {
            'size': (width, height),
            'crop': crop,
            'upscale': upscale,
        }
        return options
        
    
            
    
    @property
    def img_placeholder(self):
        # we want the base64 picture to take priority by design
        if self.placeholder_base64_picture:
            return self.placeholder_base64_picture
        # picture can be empty, for example when the image is removed from filer
        # in this case we want to return an empty string to avoid #69
        elif not self.placeholder_picture:
            return ''
        # return the original, unmodified picture
        elif self.use_no_cropping:
            return self.placeholder_picture.url

        picture_options = self.get_placeholder_size(
            width=self.width or 0,
            height=self.height or 0,
        )

        thumbnail_options = {
            'size': picture_options['size'],
            'crop': picture_options['crop'],
            'upscale': picture_options['upscale'],
            'subject_location': self.placeholder_picture.subject_location,
        }

        thumbnailer = get_thumbnailer(self.placeholder_picture)
        return thumbnailer.get_thumbnail(thumbnail_options).url
    
    
    class Meta:
        abstract = False



@plugin_pool.register_plugin
class LazyPicturePlugin(CMSPluginBase):
    model = LazyPicture
    name = "Lazy Picture"
    
    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_picture/{}/picture.html'.format(instance.template)

    def render(self, context, instance, placeholder):
        
        classes = 'lazy img-fluid '
        if instance.alignment:
            # Set the class attribute to include the alignment html class
            # This is done to leverage the attributes_str property
            classes += 'align-{} '.format(instance.alignment)
            
        classes += instance.attributes.get('class', '')
        instance.attributes['class'] = classes
        
        # assign link to a context variable to be performant
        context['picture_link'] = instance.get_link()
        context['picture_size'] = instance.get_size(
            width=context.get('width') or 0,
            height=context.get('height') or 0,
        )
        context['img_srcset_data'] = instance.img_srcset_data

        return super(LazyPicturePlugin, self).render(context, instance, placeholder)
