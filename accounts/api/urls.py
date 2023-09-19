from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.UserRegistrationView.as_view(),name='register' ),
    path('verify_email/',views.VerifyEmailView.as_view(),name='verify-email'),
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
]
