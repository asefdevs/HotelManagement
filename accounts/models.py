from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(
        max_length=64, blank=True, null=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    profile_photo = models.ImageField(
        null=True, blank=True, upload_to='profile_photos')
    citizenship = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_photo:
            img = Image.open(self.profile_photo.path)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.profile_photo.path)

    def __str__(self):
        return self.user.username