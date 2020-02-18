import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Profile
from .models import TutorCourse
from .models import StudentCourse

class ProfileModelTests(TestCase):
#TEST must begin with the string test
    def test_username_string(self):
        """
        input username is returned by to string method
        """
        p = Profile(username="holly")
        self.assertEqual(p.__str__(), "holly")