from accounts.models import Profile,CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.tasks import send_reservation_info
from hotel.models import Reservation

@receiver(post_save,sender=CustomUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
            Profile.objects.create(user=instance)



@receiver(post_save,sender=Reservation)
def reservation_info(sender,instance,created,**kwargs):
    if created:
        send_reservation_info.delay(
                                    start_date=instance.start_date,end_date=instance.end_date,
                                    room=instance.room.id,total_price=instance.total_price,
                                    email_to=instance.host.email
                                    )
