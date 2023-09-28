from accounts.models import Profile,CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.tasks import send_mail_to_subscribers
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import secrets


@receiver(post_save,sender=CustomUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
            Profile.objects.create(user=instance)



