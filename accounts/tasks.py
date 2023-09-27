from celery import shared_task
from .models import CustomUser
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def send_mail_to_subscribers():
    email_list = CustomUser.objects.filter(is_verified=True).values_list('email',flat=True)
    mail_text = f"Hello, <br> Thanks for choosing us ! <br> Thanks, <br> <h1>Hotel</h1>"

    msg = EmailMultiAlternatives(subject='Welcome', body=mail_text, from_email=settings.EMAIL_HOST_USER, to=email_list, )
    msg.attach_alternative(mail_text, "text/html")
    msg.send()


send_mail_to_subscribers.delay()

# sleep 10 seconds
# import time
# @shared_task
# def process():
#     time.sleep(10)
#     return "Hello World"