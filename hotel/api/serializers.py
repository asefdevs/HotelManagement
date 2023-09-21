from rest_framework import serializers
from hotel.models import *


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    guests = GuestSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ('start_date', 'end_date', 'total_price', 'host', 'room', 'guests')

    def create(self, validated_data):
        guests_data = validated_data.pop('guests')
        reservation = Reservation.objects.create(**validated_data)

        for guest_data in guests_data:
            guest=Guest.objects.create(reservation=reservation, **guest_data)
            reservation.guests.add(guest) 
        if reservation.start_date and reservation.end_date and reservation.room and reservation.room.price_per_night is not None:
            duration = (reservation.end_date - reservation.start_date).days
            if duration:
                reservation.total_price = duration * reservation.room.price_per_night
            else:
                reservation.total_price = None
        else:
            reservation.total_price = None
        return reservation
