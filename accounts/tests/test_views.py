from rest_framework.test import APITestCase,APIClient
from accounts.models import CustomUser
from rest_framework.authtoken.models import Token
from django.urls import reverse,resolve
from rest_framework import status
class TestViews(APITestCase):
    url=reverse('photo-update')
    url_detail=reverse('profile-detail',args=[1])

    def setUp(self):
        self.user=CustomUser.objects.create(username='testuser1',email='test@mail.com',is_verified=True)
        self.user.set_password('testpassword1')
        self.user.save()
        self.token=Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)


    def test_user_authectication(self):
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_user_unauthenticated(self):
        self.client.force_authenticate(user=None,token=None)
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail(self):
        response=self.client.get(self.url_detail)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_login_user(self):
        url = reverse('custom_login')
        data = {
            "username": "testuser1",
            "password": "testpassword1",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

