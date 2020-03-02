import datetime
from django.test import TestCase, Client, LiveServerTestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, TutorCourse, StudentCourse, MobileNotification, InAppMessage
from login.views import *
from login.forms import UserForm, ProfileForm
from selenium import webdriver
import time


class UserModelTests(TestCase):
#TEST must begin with the string test
    def test_username_string(self):
        """
        input username is returned by to string method
        """
        tester = User(email="tester@virginia.edu")
        self.assertEqual(tester.__str__(), "")

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
        course = "CBNameTutor:CS 1110 - Introduction to Programming"
        parsed = parseCourse(course)
        self.assertEqual(parsed[0], 'CS')
        self.assertEqual(parsed[1], '1110')
        self.assertEqual(parsed[2], 'Introduction to Programming')

    def test_saveClasses(self):
        c = Client()
        postedItems = {'CBNameTutor:CS 3240 - Advanced Software Development Techniques': 'new'}
        tester = User.objects.create(username='tester', password='12345', is_active=True, is_staff=True, is_superuser=True)
        tester.save()
        c.login(username='tester', password='12345')
        saveClasses(postedItems.items(), tester.id)
        self.assertNotEqual(len(TutorCourse.objects.filter(user=tester.profile)), 0)
        tester.delete()

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
        self.assertEqual(tester.profile.phone_number, "3018523444")
        tester.delete()
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

# class UpdateProfileTests(LiveServerTestCase):
#     port = 8000
#     def test_update_profile(self):
#         driver = webdriver.Chrome()
#         my_admin = User.objects.create_superuser('matt', 'mjh3nv@virginia.com', 'abc123')
#         c = Client()
#         c.login(username='matt', password='kmbba123')
#         driver.get(self.live_server_url + '/admin/')
#         username = driver.find_element_by_name('username')
#         username.send_keys('matt')
#         password = driver.find_element_by_name('password')
#         password.send_keys('abc123')
#         password.submit()
#         time.sleep(1)
#         driver.get(self.live_server_url)
#         time.sleep(1)
#         profileButton = driver.find_element_by_xpath('//*[@id="navbarNav"]/ul/li[4]')
#         profileButton.click()
#         time.sleep(1)
#         first_name = driver.find_element_by_name('first_name')
#         first_name.send_keys('Matthew')
#         time.sleep(1)
#         last_name = driver.find_element_by_name('last_name')
#         time.sleep(1)
#         last_name.send_keys('Hunt')
#         username = driver.find_element_by_name('username')
#         time.sleep(1)
#         username.send_keys('matthuntt')
#         phone_number = driver.find_element_by_name('phone_number')
#         time.sleep(1)
#         phone_number.send_keys('3018523444')
#         studentAdd = driver.find_element_by_xpath('/html/body/div/form/div[2]/div[1]/div[1]/span')
#         tutorAdd = driver.find_element_by_xpath('/html/body/div/form/div[2]/div[2]/div[1]/span')
#         time.sleep(1)
#         studentAdd.click()
#         input = driver.find_element_by_id('course')
#         input.send_keys('CS 3240')
#         time.sleep(1)
#         phone_number.submit()
#         time.sleep(1)
#         profileButton = driver.find_element_by_xpath('//*[@id="navbarNav"]/ul/li[4]')
#         profileButton.click()
#         time.sleep(10)
#         driver.close()

class MobileNotificationModelTests(TestCase):
#TEST must begin with the string test
    def test_username_string(self):
        """
        input username is returned by to string method
        """
        p = Profile(username="holly")
        self.assertEqual(p.__str__(), "holly")

class InAppMessageModelTests(TestCase):
#TEST must begin with the string test
    def test_username_string(self):
        """
        input username is returned by to string method
        """
        p = Profile(username="holly")
        self.assertEqual(p.__str__(), "holly")
