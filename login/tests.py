import datetime
import unittest
from django.test import Client
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Profile
from .models import TutorCourse
from .models import StudentCourse
from allauth.account.forms import BaseSignupForm, ResetPasswordForm, SignupForm
from allauth.account.models import (
    EmailAddress,
    EmailConfirmation,
    EmailConfirmationHMAC,
)


class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_main(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
    def test_profile(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
class SimpleTest2(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
    def test_redirect(self):
        response = self.client.get('/profile')
        self.assertRedirects(response, '/accounts/login/?next=/profile', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
"""
from allauth.tests import Mock, TestCase, patch
from allauth.utils import get_user_model, get_username_max_length
from allauth.tests import Mock, TestCase, patch
from allauth.utils import get_user_model, get_username_max_length
from allauth.tests import MockedResponse, mocked_response

from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate
 
 
class TestGoogleLogin(StaticLiveServerTestCase):
 
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.wait = WebDriverWait(self.browser, 10)
        activate('en')
 
    def tearDown(self):
        self.browser.quit()
 
    def get_element_by_id(self, element_id):
        return self.browser.wait.until(EC.presence_of_element_located(
                (By.ID, element_id)))
 
    def get_button_by_id(self, element_id):
        return self.browser.wait.until(EC.element_to_be_clickable(
                (By.ID, element_id)))
 
    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)
 
    def test_google_login(self):
        self.browser.get(self.get_full_url("home"))
        google_login = self.get_element_by_id("google_login")
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("logout")
        self.assertEqual(
            google_login.get_attribute("href"),
            self.live_server_url + "/accounts/google/login")
        google_login.click()
        with self.assertRaises(TimeoutException):
            self.get_element_by_id("google_login")
        google_logout = self.get_element_by_id("logout")
        google_logout.click()
        google_login = self.get_element_by_id("google_login")
        
from django.contrib.auth import get_user_model 

class TestAllauth(TestCase):

    def test_signup(self):
        username = 'testuser'
        password = 'testpass'
        User = get_user_model()
        user = User.objects.create_user(username, password=password)
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)
"""
class ProfileModelTests(TestCase):
#TEST must begin with the string test
    def test_username_string(self):
        """
        input username is returned by to string method
        """
        p = Profile(username="holly")
        self.assertEqual(p.__str__(), "holly")

