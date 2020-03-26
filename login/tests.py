import datetime
from django.utils import timezone
from django.urls import reverse
from django.test import TestCase, Client, LiveServerTestCase
from django.contrib.auth.models import User
from .models import Profile, TutorCourse, StudentCourse
from login.views import *
from login.forms import UserForm, ProfileForm
import unittest
import time

class ProfileModelTests(TestCase):
#TEST must begin with the string test
    def test_username_string(self):
        """
        input username is returned by to string method
        """
        p = Profile(username="holly")
        self.assertEqual(p.__str__(), "holly")
class UserModelTests(TestCase):
#TEST must begin with the string test
    def test_username_string(self):
        """
        input username is returned by to string method
        """
        tester = User(email="tester@virginia.edu")
        self.assertEqual(tester.__str__(), "")

class SimpleLogin(unittest.TestCase):
    def setUp(self):
        person = Profile(username = 'holly')

class ClassFileTests(TestCase):
    def test_userForm(self):
        c = Client()
        tester = User.objects.create(username='tester', password='12345', is_active=True, is_staff=True, is_superuser=True)
        tester.save()
        c.login(username='tester', password='12345')
        form = UserForm({
            'first_name': "tester2",
            'last_name': "lastname",
        }, instance=tester)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(tester.first_name, "tester2")
        self.assertEqual(tester.last_name, "lastname")
        tester.delete()

    def test_profileForm(self):
        c = Client()
        tester = User.objects.create(username='tester', password='12345', is_active=True, is_staff=True, is_superuser=True)
        tester.save()
        c.login(username='tester', password='12345')
        form = ProfileForm({
            'username': "tester",
            'phone_number': "3018523444",
        }, instance=tester.profile)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(tester.profile.username, "tester")
        tester.delete()
    
    def test_profileAndLogin(self):
        c = Client()
        tester = User.objects.create(username='tester', password='12345', is_active=True, is_staff=True, is_superuser=True)
        tester.save()
        self.assertFalse(c.login(username='test', password='1234'))
        tester.delete()
class HomepageTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_main(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
    def test_profile(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
class RedirectTests(TestCase):
    def setUp(self):
        self.client = Client()
    def test_redirect(self):
        response = self.client.get('/profile')
        self.assertRedirects(response, '/accounts/login/?next=/profile', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
