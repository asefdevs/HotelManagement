from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('verify_email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('login/', views.CustomAuthToken.as_view(), name='custom_login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('celery/', views.YourNewView.as_view(),name='celery'),
]
