from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Name')}),
            'phone': forms.TextInput(attrs={'placeholder': _('Phone Number')}),
            'email': forms.TextInput(attrs={'placeholder': _('Email')}),
            'message': forms.Textarea(attrs={'placeholder': _('Message')}),
        }
    
    def save(self, commit=True):
        instance = super(MessageForm, self).save(commit)
        return instance
