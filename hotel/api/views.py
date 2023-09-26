from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework import generics
from datetime import datetime, timedelta, timezone
from rest_framework.views import APIView
from hotel.models import *
from rest_framework import permissions
from .pagination import CustomPagination
from .permissions import *
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class CreateHotelView(generics.CreateAPIView):

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        hotel_name = 'Asef Hotel'
        name = self.request.data.get('name', '')
        serializer.save(name=f'{hotel_name} -{name}')


class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]


class CreateListRoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    pagination_class = CustomPagination


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]


class ListGuestView(generics.ListAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [permissions.IsAdminUser]


class RecentReservationsView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Reservation.objects.filter(
            host=self.request.user).order_by('-id')
        return queryset


class ReservationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsReservationOwner]

    def get_object(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        self.check_object_permissions(self.request, reservation)
        return reservation

    def check_time_difference(self, reservation):
        date_now = datetime.now()
        end_date = reservation.end_date.replace(tzinfo=None)
        time_delta = end_date-date_now
        if time_delta < timedelta(days=2):
            raise ValidationError(
                "You can't change or delete your reservation less than 2 days before the end date")

        print(time_delta)

    def get(self, request, pk):
        try:
            reservation = self.get_object(request, pk)
            serializer = ReservationSerializer(reservation)
        except:
            return Response(
                {'error': 'Reservation does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            reservation = self.get_object(request, pk)
        except Reservation.DoesNotExist:
            return Response(
                {'error': 'Reservation does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            self.check_time_difference(reservation)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = self.get_object(request, pk)
        if not reservation:
            return Response(
                {'error': 'Reservation does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            self.check_time_difference(reservation)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        reservation.delete()
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_204_NO_CONTENT)


class CreateReservationView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        guests_data = self.request.data.get('guests')
        user = self.request.user
        reservation = serializer.save(host=user)
        if guests_data:
            for guest_data in guests_data:
                guest = Guest.objects.create(
                    reservation=reservation, **guest_data)
                guest.save()
                reservation.guests.add(guest)


class FilterAvaibleRoomsView(APIView):
    serializer_class = ListAvaibleRoomsSerializer
    permission_classes = [IsAdminOrReadOnlyPermission]
    pagination_class = CustomPagination

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
