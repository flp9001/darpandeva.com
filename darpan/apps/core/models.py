from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class Message(models.Model):
    name = models.CharField(_("Name"), max_length=256, null=False)
    phone = models.CharField(_("Phone Number"), max_length=32, null=False)
    email = models.EmailField(_("Email"), help_text="", )
    message = models.TextField(_("Message"), null=False)
    
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse("core:message-detail", kwargs={"pk":self.pk})
    
    def __str__(self):
        message = self.message
        date = str(self.created.date())
        if len(message)>32:
            message = message[:32] + '...'
        return "{0} {1}: {2}".format(date, self.name, message)
        
    def send_email(self):
        message = Mail(
            from_email=self.email,
            to_emails='darpan.deva.tantra@gmail.com',
            subject='Contato %s - %s' % (self.name, self.phone),
            html_content=self.message)
        
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
        else:
            print("Email sent successfully")
            
    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)



#@receiver(post_save, sender=Message)
def send_email(sender, instance, created, **kwargs):
    message = Mail(
            from_email=instance.email,
            to_emails='darpan.deva.tantra@gmail.com',
            subject='[DD-WS] %s - %s' % (instance.name, instance.phone),
            html_content=instance.message)
        
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    else:
        print("Email sent successfully")
