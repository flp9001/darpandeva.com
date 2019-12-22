from django.shortcuts import redirect
from django.views import generic
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .models import LinkAccess
from .forms import ContactForm

def linkView(request, target):
    url = request.GET['url']
    link_access = LinkAccess.objects.create(name=target, url=url)
    link_access.save()
    print("Redirecting to", url)
    return redirect(url)


#def contactView(request):
#    print("I got the form")


#class MessageCreate(generic.edit.CreateView):
class MessageCreate(generic.FormView):
    template_name = 'contact_form/contact_plugin.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        messages.success(self.request, _('Message Sent'))
        return super().form_valid(form)
