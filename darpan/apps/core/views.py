from django.shortcuts import render
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlencode
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

from .models import Message
from .forms import MessageForm

class MessageCreate(generic.edit.CreateView):
    form_class = MessageForm
    template_name = 'core/message_form.html'
    success_url = '.'
    
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        #self.object = form.save()
        messages.success(self.request, _('Message Sent'))
        return super().form_valid(form)


class MessageDetail(generic.DetailView):
    model = Message

class MessageList(generic.ListView):
    model = Message


def whatsappView(request):
    params = {
        "phone":"5511930628878",
        "text": "Olá Darpan tudo bem? Achei seu contato no seu site e gostaria de algumas informações..."
    }
    
    url = "https://api.whatsapp.com/send"
    url += '?' + urlencode(params)
    
    return redirect(url)


def telegramView(request):
    url = "https://t.me/DarpanDevaTantra"
    
    return redirect(url)
