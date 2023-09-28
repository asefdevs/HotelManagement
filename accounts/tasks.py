from celery import shared_task
from .models import CustomUser
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def send_mail_to_subscribers(email_to, verification_link):
    mail_text = f"Hello, <br> Thanks for choosing us ! <br> Please click the link below for activate your profile  <br> <br>{verification_link}<br> <h1>Hotel</h1>"

    msg = EmailMultiAlternatives(
        subject='Welcome', body=mail_text, from_email=settings.EMAIL_HOST_USER, to=[email_to], )
    msg.attach_alternative(mail_text, "text/html")
    msg.send()


@shared_task
def send_reservation_info(start_date, end_date, room, total_price,email_to):
    print(f"Total Price in send_reservation_info: {total_price}")  
    mail_text = (
        'Welcome, here is your reservation details ! <br>'
        f'Reservation start date: {start_date}<br>'
        f'Reservation end date: {end_date}<br>'
        f'Room number: {room}<br>'
        f'Total price: {total_price}<br>'
    )
    msg=EmailMultiAlternatives(
        subject='Successfully Reserved',body=mail_text,from_email=settings.EMAIL_HOST_USER,to=[email_to],)
    msg.attach_alternative(mail_text,"text/html")
    msg.send()
    
