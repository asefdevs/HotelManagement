from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework import generics
from django.urls import reverse
from django.shortcuts import redirect
import secrets
from accounts.models import CustomUser
from django.contrib.sites.shortcuts import get_current_site
from dj_rest_auth.views import LoginView as RestLogin
from django.core.mail import send_mail
from django.conf import settings
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = secrets.token_urlsafe(32)
            user.email_verification_token = token
            user_email=user.email
            user.save()
            current_site = get_current_site(request).domain
            relativeLink = reverse('verify-email')
            verification_link = 'http://'+current_site+relativeLink+"?token="+str(token)
            send_mail(
                'Verify your email address',
                f'Please verify your email address by clicking the link {verification_link}.',
                'settings.EMAIL_HOST_USER',
                [user_email],
                fail_silently=False)


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            user = CustomUser.objects.get(email_verification_token=token)
            user.is_verified = True
            user.email_verification_token = None
            user.save()
            return Response({'message': 'Successfully verified'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid token or user not found'}, status=status.HTTP_404_NOT_FOUND)

class CustomLoginView(RestLogin):
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        
        user = self.serializer.validated_data['user']
        
        if not user.is_verified:
            return Response({'detail': 'User is not verified.'}, status=status.HTTP_403_FORBIDDEN)

        self.login()
        return self.get_response()