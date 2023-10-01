from django.urls import reverse,resolve
from django.test import SimpleTestCase
from accounts.api.views import  *

class TestUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url=reverse('register')
        self.assertEquals(resolve(url).func.view_class,UserRegistrationView)

    def test_verify_email_resolves(self):
        url=reverse('verify-email')
        self.assertEquals(resolve(url).func.view_class,VerifyEmailView)
    
    def test_login_url_resolves(self):
        url=reverse('custom_login')
        self.assertEquals(resolve(url).func.view_class,CustomAuthToken)

    def test_logout_url_resolves(self):
        url=reverse('logout')
        self.assertEquals(resolve(url).func.view_class,LogoutView)
    
    def test_profile_details_url_resolves(self):
        url=reverse('profile-detail',args=['1'])
        self.assertEquals(resolve(url).func.view_class,ProfileDetails)

    def test_profile_photo_url_resolves(self):
        url=reverse('photo-update')
        self.assertEquals(resolve(url).func.view_class,ProfilePhotoUpdate)

    