from django.urls import path
from . import views

urlpatterns = [
    path('hotels/', views.CreateHotelView.as_view(), name='hotel-list-create'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel-detail'),
    path('rooms/', views.CreateListRoomView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('guests/', views.ListGuestView.as_view(), name='guest-list'),
    path('reservations/', views.CreateReservationView.as_view(),
         name='reservation-list-create'),
    path('reservations/<int:pk>/', views.ReservationDetailView.as_view(),
         name='reservation-detail'),
    path('recent_reservations/', views.RecentReservationsView.as_view(),
         name='recent-reservations'),
    path('available_rooms/', views.FilterAvailableRoomsView.as_view(), name='available-rooms')
]
