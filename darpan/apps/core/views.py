from django.shortcuts import render
from django.views import generic
# Create your views here.

from .models import Message

class MessageCreate(generic.edit.CreateView):
    model = Message
    fields = '__all__'


class MessageDetail(generic.DetailView):
    model = Message

class MessageList(generic.ListView):
    model = Message
