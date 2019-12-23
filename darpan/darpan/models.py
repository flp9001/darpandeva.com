from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
    sent = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse("darpan:message-detail", kwargs={"pk":self.pk})
    
    def __str__(self):
        message = self.message
        date = str(self.created.date())
        if len(message)>32:
            message = message[:32] + '...'
        return "{0} {1}: {2}".format(date, self.name, message)
        



@receiver(post_save, sender=Message)
def send_email(sender, instance, created, **kwargs):
    if not instance.sent:
        user = get_user_model().objects.filter(is_superuser=True).first()
        email = user.email if user else 'contato@darpandeva.com'
        
        message = Mail(
                from_email=instance.email,
                to_emails=email,
                subject='[DD-WS] %s - %s' % (instance.name, instance.phone),
                html_content=instance.message)
            
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
        except Exception as e:
            print(e)
        else:
            print("Email sent successfully")
            instance.sent = True
            post_save.disconnect(send_email, sender=Message)
            instance.save()
            post_save.connect(send_email, sender=Message)
