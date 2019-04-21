from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Message(models.Model):
    name = models.CharField(_("Name"), max_length=256, null=False)
    phone = models.CharField(_("Phone Number"), max_length=32, null=False)
    email = models.EmailField(_("Email"), help_text="", )
    message = models.TextField(_("Message"), null=False)
    
    created = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse("core:message-detail", kwargs={"date": self.created, "pk":self.pk})
    
    def __str__(self):
        message = self.message
        date = str(self.created.date())
        if len(message)>32:
            message = message[:32] + '...'
        return "{0} {1}: {2}".format(date, self.name, message)
