from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('verify_email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('login/', views.CustomAuthToken.as_view(), name='custom_login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:id>/', views.ProfileDetails.as_view(),name='profile-detail'),
    path('profile/photo_update/',views.ProfilePhotoUpdate.as_view(),name='photo-update'),
]
