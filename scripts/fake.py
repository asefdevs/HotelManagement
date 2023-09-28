
import random

from hotel.models import Hotel, Room
from faker import Faker
fake = Faker()

def generate_fake_data(num_hotels=5, num_rooms_per_hotel=10):
    hotels = []
    for _ in range(num_hotels):
        hotel = Hotel(
            name=fake.company(),
            address=fake.address(),
            city=fake.city(),
            country=fake.country(),
            phone=fake.phone_number(),
            email=fake.email(),
            social_media=fake.url(),
            about=fake.paragraph()
        )
        hotel.save()
        hotels.append(hotel)

    for hotel in hotels:
        for _ in range(num_rooms_per_hotel):
            room = Room(
                hotel=hotel,
                room_number=random.randrange(1, 10),
                room_type=random.choice(['1', '2', '3', '4', '5']),
                bed_type=fake.word(),
                description=fake.paragraph(),
                price_per_night=random.uniform(50, 300),
                is_available=True
            )
            room.save()



