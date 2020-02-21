from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.urls import reverse
import json
import requests
from django.views.generic import View
from bs4 import BeautifulSoup
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from fcm_django.models import FCMDevice
from .models import Profile, StudentCourse, TutorCourse, MobileNotification
from login.serializers import ProfileSerializer, StudentCourseSerializer, TutorCourseSerializer
from .tasks import send_new_message_push_notification

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Signed out')
        return HttpResponseRedirect(reverse('login:home', args=()))

def renderTutorPage(request):
    if not request.user.is_authenticated:
        return render(request, 'login/tutorSearch.html')
    else:
        classes = get_classes_fromtxt()
        student_courses = list(StudentCourse.objects.filter(user=request.user.profile))
        tutor_courses = list(TutorCourse.objects.filter(user=request.user.profile))
        profile = json.dumps(ProfileSerializer(request.user.profile).data)
        filtered_tutors = []
        for i in range(len(student_courses)):
            student_courses[i] = StudentCourseSerializer(student_courses[i]).data
        for i in range(len(tutor_courses)):
            tutor_courses[i] = TutorCourseSerializer(tutor_courses[i]).data
        if request.method == 'POST' and request.is_ajax():
            course = request.POST.get('course', "")
            pushToken_registration = json.loads(request.POST.get('pushToken_registration', '{}'))
            print(pushToken_registration)
            if course == "" and not bool(pushToken_registration):
                courses = json.loads(request.POST.get('courses', []))
                course_names = []
                for class_ in courses:
                    course_names.append(class_['name'])
                filtered_tutors = list(Profile.objects.filter(tutorcourse__name__in=course_names))
            elif course != "":
                course = course.split('-')[1].lstrip()
                filtered_tutors = list(Profile.objects.filter(tutorcourse__name=course))
            elif bool(pushToken_registration):
                sender = request.user
                recipient = request.user
                request.user.profile.push_token = pushToken_registration['registration_id']
                request.user.profile.save()
                try:
                    device = FCMDevice.objects.get(device_id=request.user.id)
                    device.registration_id=pushToken_registration['registration_id']
                    device.type=pushToken_registration['type']
                    device.save()
                except:
                    FCMDevice(user=request.user, registration_id=pushToken_registration['registration_id'], type=pushToken_registration['type'], device_id=request.user.id, name=request.user.email).save()
                return JsonResponse({'registration_id': pushToken_registration['registration_id'], 'type': pushToken_registration['type'], 'profile': profile, 'filtered_tutors': filtered_tutors, 'course': course})
            for i in range(len(filtered_tutors)):
                filtered_tutors[i] = ProfileSerializer(filtered_tutors[i]).data
            return JsonResponse({'profile': profile, 'filtered_tutors': filtered_tutors, 'course': course})
        return render(request, 'login/tutorSearch.html', {'profile': profile, 'classes': classes})

@login_required
@transaction.atomic
def update_profile(request):
    classes = get_classes_fromtxt()
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        saveClasses(request.POST.items(), request.user.profile.id)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated')
            return redirect('login:home')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'login/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'classes': classes
    })

def saveClasses(postedItems, user_id):
    for key, value in postedItems:
        if(key.startswith('CBNameTutor')):
            if(value == 'new'):
                (dept, number, name) = parseCourse(key)
                tutor_course = TutorCourse(dept=dept, number=number, name=name, user_id=user_id)
                tutor_course.save()
            elif value != 'recentlyAdded':
                TutorCourse.objects.filter(id=value).delete()
        if(key.startswith('CBNameStudent')):
            if(value == 'new'):
                (dept, number, name) = parseCourse(key)
                student_course = StudentCourse(dept=dept, number=number, name=name, user_id=user_id)
                student_course.save()
            elif value != 'recentlyAdded':
                StudentCourse.objects.filter(id=value).delete()

class ServiceWorkerView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login/firebase-messaging-sw.js', content_type="application/x-javascript")

def parseCourse(course_name):
    course = course_name.split(':')[1]
    parts = course.split('-')
    dept_number = parts[0].rstrip()
    name = parts[1].lstrip()
    dept_parts = dept_number.split(' ')
    dept = dept_parts[0]
    number = dept_parts[1]
    return (dept, number, name)

def schools(request):
    classes = get_classes_fromtxt()
    school_data = get_schools_fromtxt()
    school_list = list(school_data.keys())
    section_list = list(school_data.values())
    return render(request, 'login/schools.html', {'school_list': school_list, 'section_list': section_list, 'classes': classes})

def courses(request):
    courses = request.session['courses']
    return render(request, 'login/courses.html', {'courses':courses})

def get_section(request):
    try:
        courses = []
        link = request.POST['choice']
        courses = get_courses(link)
        request.session['courses'] = json.dumps(courses)
    except:
        school_data = get_schools_fromtxt()
        school_list = list(school_data.keys())
        section_list = list(school_data.values())
        return render(request, 'login/schools.html', {'school_list': school_list, 'section_list': section_list})
    return HttpResponseRedirect(reverse('login:courses'))

def get_courses(url):
    link = url
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        classes = []
        try:
            names = soup.find_all( class_="CourseName")
            for name in names:
                parts = name.get('onclick').split(',')
                dept = parts[0].split("'")[1]
                number = parts[1].split("'")[1]
                course_name = name.get_text()
                classes.append((dept, number, course_name))
        except:
            None
        return classes
    else:
        return []

def get_schools_fromtxt():
    with open('staticfiles/login/class_sections.txt') as json_file:
        schools = json.load(json_file)
        return schools

def get_classes_fromtxt():
    with open('staticfiles/login/classes.txt') as json_file:
        data = json.load(json_file)
        return json.dumps(data)
