from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework import generics
from datetime import datetime
from rest_framework.views import APIView
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


class CreateReservationView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class FilterAvaibleRoomsView(APIView):
    serializer_class = ListAvaibleRoomsSerializer

    def get(self, request):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        if start_date_str is not None and end_date_str is not None:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            occupied_rooms = Room.objects.filter(
                Q(room_reservation__start_date__lte=start_date, room_reservation__end_date__gte=start_date) |
                Q(room_reservation__start_date__lte=end_date, room_reservation__end_date__gte=end_date) |
                Q(room_reservation__start_date__gte=start_date,
                  room_reservation__end_date__lte=end_date)
            )

            available_rooms = Room.objects.exclude(
                id__in=occupied_rooms.values_list('id', flat=True))

            serializer = self.serializer_class(available_rooms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'Warning': 'Choose date range'},
                status=status.HTTP_400_BAD_REQUEST
            )
