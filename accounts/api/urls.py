from django.urls import path
from . import views
from dj_rest_auth.views import LogoutView
urlpatterns = [
    path('register/',views.UserRegistrationView.as_view(),name='register' ),
    path('verify_email/',views.VerifyEmailView.as_view(),name='verify-email'),
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
