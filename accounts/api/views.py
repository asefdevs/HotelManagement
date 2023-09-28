from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer, ProfilePhotoUpdateSerializer
from rest_framework import generics
from django.urls import reverse
from django.shortcuts import redirect
import secrets
from accounts.models import CustomUser, Profile
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsProfileOwner
from accounts.tasks import send_mail_to_subscribers


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = secrets.token_urlsafe(32)
            user_email=user.email
            user.email_verification_token = token
            user.save()
            current_site = get_current_site(request).domain
            relativeLink = reverse('verify-email')
            verification_link = 'http://'+current_site + \
                relativeLink+"?token="+str(token)
            send_mail_to_subscribers.delay(user_email, verification_link)
            # send_mail(
            #     'Verify your email address',
            #     f'Please verify your email address by clicking the link {verification_link}.',
            #     'settings.EMAIL_HOST_USER',
            #     [user_email],
            #     fail_silently=False)

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


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CustomAuthToken(ObtainAuthToken, generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_verified:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response({'detail': 'User is not verified'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileDetails(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwner]

    def get_object(self):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Profile.DoesNotExist
        return profile


class ProfilePhotoUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = ProfilePhotoUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response('Profile doesnt exist')
        return profile
