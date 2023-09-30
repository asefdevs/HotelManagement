from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from hotel.models import Reservation
from datetime import timedelta, datetime


@shared_task
def send_mail_to_subscribers(email_to, verification_link):
    mail_text = f"Hello, <br> Thanks for choosing us ! <br> Please click the link below for activate your profile  <br> <br>{verification_link}<br> <h1>Hotel</h1>"

    msg = EmailMultiAlternatives(
        subject='Welcome', body=mail_text, from_email=settings.EMAIL_HOST_USER, to=[email_to], )
    msg.attach_alternative(mail_text, "text/html")
    msg.send()


@shared_task
def send_reservation_info(start_date, end_date, room, total_price, email_to):
    mail_text = (
        'Welcome, here is your reservation details ! <br>'
        f'Reservation start date: {start_date}<br>'
        f'Reservation end date: {end_date}<br>'
        f'Room number: {room}<br>'
        f'Total price: {total_price}<br>'
    )
    msg = EmailMultiAlternatives(
        subject='Successfully Reserved', body=mail_text, from_email=settings.EMAIL_HOST_USER, to=[email_to],)
    msg.attach_alternative(mail_text, "text/html")
    msg.send()


@shared_task
def daily_check_task():
    today = datetime.now().date()
    reservations = Reservation.objects.filter(
        is_active=True, end_date__date__lte=today)
    if reservations:
        for reservation in reservations:
            reservation.is_active = False
            reservation.save()


@shared_task
def reservation_defore_end():
    day_before = datetime.now().date()+timedelta(days=2)
    reservations = Reservation.objects.filter(
        is_active=True, end_date__date=day_before)
    if reservations:
        for reservation in reservations:
            mail_text = (
                f'You have 2 day left for {reservation.id}-{reservation.start_date}-{reservation.end_date}')
            msg = EmailMultiAlternatives(
                subject='Reservation Notification', body=mail_text, from_email=settings.EMAIL_HOST_USER, to=[reservation.host.email],)
            msg.attach_alternative(mail_text, "text/html")
            msg.send()
