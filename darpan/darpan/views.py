from django.shortcuts import redirect
from django.views import generic
from django.contrib import messages
from django.conf import settings
from constance import config
from django.utils.translation import ugettext_lazy as _

from .models import LinkAccess
from .forms import ContactForm

def linkView(request, target):
    url = request.GET.get("url", None)
    if url is None:
        settings_name = "%s_URL" % target.upper()
        url = getattr(config, settings_name, None)
        
    if url:
        link_access = LinkAccess.objects.create(name=target, url=url)
        link_access.save()
        return redirect(url)
    else:
        return redirect('/')



class MessageCreate(generic.FormView):
    template_name = 'contact_form/contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        messages.success(self.request, _('Message Sent'))
        return super().form_valid(form)
