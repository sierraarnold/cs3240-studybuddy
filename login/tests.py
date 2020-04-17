import datetime
from django.test import TestCase, Client, LiveServerTestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, TutorCourse, StudentCourse, InAppMessage
from login.views import *
from login.forms import ProfileForm
from selenium import webdriver
import unittest
import time


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
    def test_get_departments_fromtxt(self):
        departments = get_departments_fromtxt()
        self.assertEqual(len(departments.keys()), 9)
        self.assertEqual(len(departments['Engineering & Applied Sciences Departments']), 11)

    def test_get_courses(self):
        departments = get_departments_fromtxt()
        engineering = departments['Engineering & Applied Sciences Departments']
        link = engineering[0][0]
        courses = get_courses(link)
        self.assertNotEqual(len(courses), 0)

    def test_get_classes_fromtxt(self):
        classes = json.loads(get_classes_fromtxt())
        self.assertEqual(len(classes.values()), 3072)

    def test_departments(self):
        c = Client()
        response = c.get(reverse('login:departments'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['department_list']), 9)
        self.assertEqual(len(response.context['department_section_list']), 9)
        self.assertEqual(len(json.loads(response.context['classes'])), 3072)

    def test_get_department_section(self):
        c = Client()
        response = c.post(reverse('login:get_department_section'), {'choice': 'https://louslist.org/page.php?Semester=1202&Type=Group&Group=CompSci'}, follow=True)
        courses = c.session['courses']
        self.assertNotEqual(len(json.loads(courses)), 0)

class ClassSaveTests(TestCase):
    def test_parseCourse(self):
        course = "Tutor:CS 1110 - Introduction to Programming"
        parsed = parseCourse(course)
        self.assertEqual(parsed[0], 'CS')
        self.assertEqual(parsed[1], '1110')
        self.assertEqual(parsed[2], 'Introduction to Programming')

    def test_saveClasses(self):
        c = Client()
        postedItems = {'Tutor:CS 3240 - Advanced Software Development Techniques': 'course'}
        tester = User.objects.create(username='tester', password='12345', is_active=True, is_staff=True, is_superuser=True)
        tester.save()
        c.login(username='tester', password='12345')
        saveClasses(postedItems.items(), tester.id)
        self.assertNotEqual(len(TutorCourse.objects.filter(user=tester.profile)), 0)
        tester.delete()

    # def test_userForm(self):
    #     c = Client()
    #     tester = User.objects.create(username='tester', password='12345', is_active=True, is_staff=True, is_superuser=True)
    #     tester.save()
    #     c.login(username='tester', password='12345')
    #     form = UserForm({
    #         'first_name': "tester2",
    #         'last_name': "lastname",
    #     }, instance=tester)
    #     self.assertTrue(form.is_valid())
    #     form.save()
    #     self.assertEqual(tester.first_name, "tester2")
    #     self.assertEqual(tester.last_name, "lastname")
    #     tester.delete()

    def test_profileForm(self):
        c = Client()
        tester = User.objects.create(username='tester', password='12345', is_active=True, is_staff=True, is_superuser=True)
        tester.save()
        c.login(username='tester', password='12345')
        form = ProfileForm({
            'first_name': "joe",
            'last_name': "joey",
            'username': "tester",
            'phone_number': "3018523444",
            'year': "Fourth",
            'bio': "testing",
            'location': "Inactive"
        }, instance=tester.profile)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(tester.profile.first_name, "joe")
        self.assertEqual(tester.profile.last_name, "joey")
        self.assertEqual(tester.profile.username, "tester")
        self.assertEqual(tester.profile.phone_number, "3018523444")
        tester.delete()

    def test_profileAndLogin(self):
        c = Client()
        tester = User.objects.create(username='tester', password='12345', is_active=True, is_staff=True, is_superuser=True)
        tester.save()
        self.assertFalse(c.login(username='test', password='1234'))
        tester.delete()

class TutorSearch(unittest.TestCase):
    def test_single_course_search(self):
        c = Client()
        tester = User.objects.create(username='tester', is_active=True, is_staff=True, is_superuser=True)
        tester.set_password('12345')
        tester.save()
        postedItems = {'Tutor:CS 3240 - Advanced Software Development Techniques': 'course'}
        c.login(username='tester', password='12345')
        saveClasses(postedItems.items(), tester.id)
        response = c.post(reverse('login:home'), {'course': 'CS 3240 - Advanced Software Development Techniques'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['filtered_tutors']), 1)
        tester.delete()
    def test_my_student_courses(self):
        c = Client()
        tester = User.objects.create(username='tester', is_active=True, is_staff=True, is_superuser=True)
        tester2 = User.objects.create(username='tester2', is_active=True, is_staff=True, is_superuser=True)
        tester.set_password('12345')
        tester.save()
        tester2.save()
        studentItems = {'Student:CS 3240 - Advanced Software Development Techniques': 'course', 'CBNameStudent:CS 1234 - Test Course': 'course'}
        tutorItems = {'Tutor:CS 3240 - Advanced Software Development Techniques': 'course'}
        saveClasses(studentItems.items(), tester.id)
        saveClasses(tutorItems.items(), tester2.id)
        c.login(username='tester', password='12345')
        studentCourses = ProfileSerializer(tester.profile).data['studentCourses']
        for i in range(len(studentCourses)):
            studentCourses[i] = StudentCourseSerializer(studentCourses[i]).data
        response = c.post(reverse('login:home'), {'courses': json.dumps(studentCourses)}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['filtered_tutors']), 1)
        tester.delete()
        tester2.delete()
    def test_request_tutor(self):
        c = Client()
        tester = User.objects.create(username='tester', is_active=True, is_staff=True, is_superuser=True)
        tester2 = User.objects.create(username='tester2', is_active=True, is_staff=True, is_superuser=True)
        tester.set_password('12345')
        tester.save()
        tester2.save()
        c.login(username='tester', password='12345')
        tutor = ProfileSerializer(tester2.profile).data
        response = c.post(reverse('login:home'), {'tutor': json.dumps(tutor)}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(bool(response.json()['tutor']), True)
        inappmessages = list(InAppMessage.objects.filter(sender=tester.id))
        inappmessages += list(InAppMessage.objects.filter(recipient=tester.id))
        self.assertNotEqual(len(inappmessages), 0)
        tester.delete()
        tester2.delete()

class HomepageTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_main(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
    def test_profile(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)

class RedirectTests(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
    def test_redirect(self):
        response = self.client.get('/profile')
        self.assertRedirects(response, '/accounts/login/?next=/profile', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class InAppMessageModelTests(TestCase):
    def test_in_app_message_model(self):
        tester = User(email="abc2@virginia.edu")
        tester2 = User(email="cba@virginia.edu", username="tester2")
        tester.save()
        tester2.save()
        inapp = InAppMessage(sender=tester.profile, recipient=tester2.profile, message= "This is a test message")
        inapp.save()
        self.assertEqual(inapp.message, "This is a test message")
        self.assertEqual(inapp.status, "unread")
class RedirectTests(TestCase):
    def setUp(self):
        self.client = Client()
    def test_redirect(self):
        response = self.client.get('/profile')
        self.assertRedirects(response, '/accounts/login/?next=/profile', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
