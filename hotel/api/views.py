from django.utils import timezone
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework import generics
from datetime import datetime
from rest_framework.views import APIView
from hotel.models import *
from rest_framework import permissions
from .pagination import CustomPagination
from .permissions import *


class CreateHotelView(generics.CreateAPIView):

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        hotel_name='Asef Hotel'
        name=self.request.data.get('name','')
        serializer.save(name=f'{hotel_name} -{name}')


class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]


class CreateListRoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    pagination_class=CustomPagination


class CreateGuestView(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [permissions.IsAdminUser]


class RecentReservationsView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class=[CustomPagination]


    def get_queryset(self):
        queryset = Reservation.objects.filter(
            host=self.request.user).order_by('-id')
        return queryset


class CreateReservationView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        guests_data = self.request.data.get('guests')
        
        reservation = serializer.save()
        
        for guest_data in guests_data:
            guest=Guest.objects.create(reservation=reservation, **guest_data)
            guest.save()
            reservation.guests.add(guest)



class FilterAvaibleRoomsView(APIView):
    serializer_class = ListAvaibleRoomsSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    pagination_class=[CustomPagination]


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

