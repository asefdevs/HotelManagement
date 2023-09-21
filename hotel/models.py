from django.db import models
from accounts.models import CustomUser
# Create your models here.


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    social_media = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='hotel_images')
    about = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        existing_instance = Hotel.objects.first()

        if existing_instance:
            self.id = existing_instance.id
            super(Hotel, self).save(*args, **kwargs)
        else:
            super(Hotel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    ROOM_TYPE_CHOICES = (
        ('1', '1 Person'),
        ('2', '2 Persons'),
        ('3', '3 Persons'),
        ('4', '4 Persons'),
        ('5', '5 Persons'),
    )

    room_type = models.CharField(
        max_length=1, choices=ROOM_TYPE_CHOICES, blank=True, null=True)
    bed_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(blank=True, null=True, upload_to='room_images')

    def __str__(self):
        return f"Room {self.room_number} - {self.hotel.name}"


class Guest(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, null=True)
    passport_id = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Reservation(models.Model):
    host = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user_reservation')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='room_reservation')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    guests = models.ManyToManyField(Guest, blank=True)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Reservation for {self.host.username} in Room {self.room.room_number}"
