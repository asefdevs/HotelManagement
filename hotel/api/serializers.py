from rest_framework import serializers
from hotel.models import *
from datetime import datetime
from django.db.models import Q


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

    def validate_name(self,value):
        if Hotel.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                {'name': 'Name already exists'})
        return value


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
        read_only_fields = ['host']

    def create(self, validated_data):
        guests_data = validated_data.pop('guests', [])
        room_type = validated_data['room'].room_type

        if len(guests_data) > int(room_type):
            raise serializers.ValidationError(
                "Too many guests for this room type")

        reservation = Reservation.objects.create(**validated_data)

        start_date = reservation.start_date
        end_date = reservation.end_date
        room = reservation.room

        if start_date and end_date and room and room.price_per_night is not None:
            duration = (end_date - start_date).days
            if duration > 0:
                reservation.total_price = duration * room.price_per_night
            else:
                reservation.total_price = room.price_per_night
        else:
            reservation.total_price = 0

        reservation.save()

        return reservation

    def update(self, instance, validated_data):
        guests_data = validated_data.pop('guests', [])
        room_type = instance.room.room_type
        if len(guests_data) > int(room_type):
            raise serializers.ValidationError(
                "Too many guests for this room type")
        start_date = validated_data.get('start_date', instance.start_date)
        end_date = validated_data.get('end_date', instance.end_date)
        room = validated_data.get('room', instance.room)
        if start_date and end_date and room and room.price_per_night is not None:
            duration = (end_date - start_date).days
            if duration > 0:
                total_price = duration * room.price_per_night
            else:
                total_price = room.price_per_night
        else:
            raise serializers.ValidationError('Cannot update the object')

        instance.start_date = start_date
        instance.end_date = end_date
        instance.room = room
        instance.total_price = total_price

        instance.save()
        instance.guests.clear()
        for guest_data in guests_data:
            guest = Guest.objects.create(**guest_data)
            instance.guests.add(guest)

        return instance

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
                raise serializers.ValidationError(
                    {'room': 'Room is occupied'})
            if start_date_str > end_date_str:
                raise serializers.ValidationError(
                    {'start_date': 'End date must be greater than start date'})

        return data


class ListAvaibleRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
