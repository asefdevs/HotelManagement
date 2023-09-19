from django.db import models

# Create your models here.
from django.contrib.auth.models import  User
from PIL import Image

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    profile_photo=models.ImageField(null=True,blank=True,upload_to='profile_photos')
    citizenship=models.CharField(max_length=255,blank=True,null=True)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.profile_photo:
            img=Image.open(self.profile_photo.path)
            if img.height > 600 or img.width > 600:
                output_size=(600,600)
                img.thumbnail(output_size)
                img.save(self.profile_photo.path)
                
    def __str__(self):
        return self.user.username