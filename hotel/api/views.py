from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework import generics

from hotel.models import *



class CreateHotelView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()  
    serializer_class = HotelSerializer

class CreateRoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()  
    serializer_class = RoomSerializer

class CreateGuestView(generics.ListCreateAPIView):
    queryset = Guest.objects.all()  
    serializer_class = GuestSerializer

class CreateReservationView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()  
    serializer_class = ReservationSerializer



