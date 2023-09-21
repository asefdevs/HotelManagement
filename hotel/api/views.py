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
from django.utils import timezone
from django.db.models import Q
class CreateReservationView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    # def get_queryset(self):
    #     reserved_rooms=Reservation.objects.filter(room_reservation__is_available=False)
    #     avaible_rooms = 
    # def get_queryset(self):
    #     queryset=Reservation.objects.filter(host=self.request.user)
    #     return queryset
    # def get_queryset(self):
    #     start_date=self.request.query_params.get('start_date')
    #     end_date=self.request.query_params.get('end_date')

    #     if start_date and end_date:
    #         reservations_loop = Q(start_date__lte=start_date, end_date__gte=start_date) | \
    #                               Q(start_date__lte=end_date, end_date__gte=end_date) | \
    #                               Q(start_date__gte=start_date, end_date__lte=end_date)
            
    #     queryset=Reservation.objects.exclude(reservations_loop).filter(host=self.request.user)
    #     return queryset
from rest_framework.filters import SearchFilter
from datetime import datetime
# class FilterAvaibleRoomsView(generics.ListAPIView):
from rest_framework.views import APIView

class FilterAvaibleRoomsView(APIView):
    serializer_class = ListAvaibleRoomsSerializer

    def get(self, request):
        # Get the start_date and end_date from the request query parameters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        # print(f' ________________{start_date_str}, {end_date_str}')

        # Check if both start_date and end_date are provided
        if not start_date_str or not end_date_str:
            return Response(
                {'error': 'Both start_date and end_date are required query parameters.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Parse the start_date and end_date strings into datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            # print(f' ________________{start_date}, {end_date}')
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Query the rooms that are available within the specified date range
        # available_rooms = Room.objects.exclude(
        #     room_reservation__start_date__lte=end_date,
        #     room_reservation__end_date__gte=start_date
        # ).all()
        occupied_rooms = Room.objects.filter(
            room_reservation__start_date=start_date,
            room_reservation__end_date=end_date
        )
        print(f' tutulan otaqlar {occupied_rooms}')
        available_rooms = Room.objects.exclude(id__in=occupied_rooms.values_list('id', flat=True))        
        print(f' uygun otaqlar{available_rooms}')

        # Serialize the available rooms and return the response
        serializer = self.serializer_class(available_rooms, many=True)
        print(f' bu serializer datasidi{serializer.data}')
        return Response(serializer.data, status=status.HTTP_200_OK)





    # def perform_create(self, serializer):
    #     serializer.save(host=self.request.user)



