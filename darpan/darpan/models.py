from django.db import models
from django.utils.translation import ugettext_lazy as _



class LinkAccessManager(models.Manager):
    def create(self, **obj_data):
        name = obj_data['name']
        url  = obj_data['url']
        link, created = ExternalLink.objects.get_or_create(name=name, url=url)
        del obj_data['name']
        del obj_data['url']
        obj_data['link'] = link
        return super().create(**obj_data) # Python 3 syntax!!



class ExternalLink(models.Model):
    name = models.CharField(
        verbose_name='Link Target',
        blank=True,
        max_length=255,
    )
    url = models.URLField()
    
    def __str__(self):
        return self.name.title()


class LinkAccess(models.Model):
    link = models.ForeignKey(ExternalLink,
        related_name="access",
        blank=True,
        on_delete=models.CASCADE,
        )
        
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = LinkAccessManager()
    
    
    def __str__(self):
        return str(self.link)
        


class Message(models.Model):
    name = models.CharField(_("Name"), max_length=256, null=False)
    phone = models.CharField(_("Phone Number"), max_length=32, null=False)
    email = models.EmailField(_("Email"), help_text="", )
    message = models.TextField(_("Message"), null=False)
    
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse("darpan:message-detail", kwargs={"pk":self.pk})
    
    def __str__(self):
        message = self.message
        date = str(self.created.date())
        if len(message)>32:
            message = message[:32] + '...'
        return "{0} {1}: {2}".format(date, self.name, message)
        

