from django.urls import path
from . import views

urlpatterns = [
    path('hotels/', views.CreateHotelView.as_view(), name='hotel-list-create'),
    path('rooms/', views.CreateRoomView.as_view(), name='room-list-create'),
    path('guests/', views.CreateGuestView.as_view(), name='guest-list-create'),
    path('reservations/', views.CreateReservationView.as_view(), name='reservation-list-create'),
]
