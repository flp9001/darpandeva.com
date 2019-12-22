from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Message


class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Name')}),
            'phone': forms.TextInput(attrs={'placeholder': _('Phone Number')}),
            'email': forms.TextInput(attrs={'placeholder': _('Email')}),
            'message': forms.Textarea(attrs={'placeholder': _('Message')}),
        }
    
    def save(self, commit=True):
        print("FORM SAVED")
        instance = super(ContactForm, self).save(commit)
        return instance
