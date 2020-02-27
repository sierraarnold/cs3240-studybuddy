import datetime

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
from allauth.tests import Mock, TestCase, patch
from allauth.utils import get_user_model, get_username_max_length
from allauth.tests import Mock, TestCase, patch
from allauth.utils import get_user_model, get_username_max_length
from allauth.tests import MockedResponse, mocked_response


class ProfileModelTests(TestCase):
#TEST must begin with the string test
    def test_username_string(self):
        """
        input username is returned by to string method
        """
        p = Profile(username="holly")
        self.assertEqual(p.__str__(), "holly")

from django.contrib.auth import get_user_model 

class TestAllauth(TestCase):

    def test_signup(self):
        username = 'testuser'
        password = 'testpass'
        User = get_user_model()
        user = User.objects.create_user(username, password=password)
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)
