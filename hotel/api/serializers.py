from rest_framework import serializers
from hotel.models import *
from datetime import datetime
from django.db.models import Q


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def validate(self, data):
        room_number = data['room_number']
        if Room.objects.filter(room_number=room_number).exists():
            raise serializers.ValidationError(
                {'room_number': 'Room number already exists'})
        return data


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    guests = GuestSerializer(many=True, required=False)

    class Meta:
        model = Reservation
        fields = '__all__'

    def create(self, validated_data):
        guests_data = validated_data.pop('guests', [])
        room_type = validated_data['room'].room_type

        if len(guests_data) > int(room_type):
            raise serializers.ValidationError(
                "Too many guests for this room type")

        reservation = Reservation.objects.create(**validated_data)

        for guest_data in guests_data:
            Guest.objects.create(reservation=reservation, **guest_data)

        start_date = reservation.start_date
        end_date = reservation.end_date
        room = reservation.room

        if start_date and end_date and room and room.price_per_night is not None:
            duration = (end_date - start_date).days
            if duration>0:
                reservation.total_price = duration * room.price_per_night
            else:
                reservation.total_price = room.price_per_night
        else:
            reservation.total_price = None

        reservation.save()

        return reservation

    def validate(self, data):
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        room = data.get('room')

        if start_date_str and end_date_str and room:

            overlapping_reservations = Reservation.objects.filter(
                Q(room=room) &
                (Q(start_date__lte=start_date_str, end_date__gte=start_date_str) |
                 Q(start_date__lte=end_date_str, end_date__gte=end_date_str) |
                 Q(start_date__gte=start_date_str, end_date__lte=end_date_str))
            )
            if overlapping_reservations.exists():
                raise serializers.ValidationError({'room': 'Room is occupied'})

            if start_date_str > end_date_str:
                raise serializers.ValidationError(
                    {'start_date': 'End date must be greater than start date'})

        return data


class ListAvaibleRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
