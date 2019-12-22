from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


from .models import Message

@receiver(post_save, sender=Message)
def send_email(sender, instance, created, **kwargs):
    message = Mail(
            from_email=instance.email,
            to_emails='contato@darpandeva.com',
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
