from rest_framework import serializers
from hotel.models import *
from datetime import datetime


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
            guest = Guest.objects.create(reservation=reservation, **guest_data)
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

    def validate(self, data):
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        room = data.get('room')

        if start_date_str and end_date_str and room:

            # Check if there are any overlapping reservations for the same room
            overlapping_reservations = Reservation.objects.filter(
                room__id=room.id,
                start_date=start_date_str,
                end_date=end_date_str,
            )
            re=Reservation.objects.last().start_date

            if overlapping_reservations.exists():
                raise serializers.ValidationError({'room': 'Room is occupied'})
            else:
                print(overlapping_reservations)
                print(room.id,start_date_str,end_date_str)
                print(re)

        if start_date_str > end_date_str:
                print(f' __======____+_+_+_+_{start_date_str}--------{end_date_str}')
                raise serializers.ValidationError({'start_date': 'End date must be greater than start date'})

        return data


    
class ListAvaibleRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
