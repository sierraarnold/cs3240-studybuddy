from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.urls import reverse
import json
import requests
from bs4 import BeautifulSoup
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .models import Profile, StudentCourse, TutorCourse
from login.serializers import ProfileSerializer, StudentCourseSerializer, TutorCourseSerializer


def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Signed out')
        return HttpResponseRedirect(reverse('login:home', args=()))

def tutor(request):
    if not request.user.is_authenticated:
        return render(request, 'login/map.html')
    else:
        classes = get_classes()
        student_courses = StudentCourse.objects.filter(user=request.user.profile)
        tutor_courses = TutorCourse.objects.filter(user=request.user.profile)
        if request.method == 'POST' and request.is_ajax():
            course = request.POST['course']
            course = course.split('-')[1].lstrip()
            filtered_tutors = Profile.objects.filter(tutorcourse__name=course)
            student_courses = list(student_courses)
            tutor_courses = list(tutor_courses)
            filtered_tutors = list(filtered_tutors)
            for i in range(len(student_courses)):
                student_courses[i] = StudentCourseSerializer(student_courses[i]).data
            for i in range(len(tutor_courses)):
                tutor_courses[i] = TutorCourseSerializer(tutor_courses[i]).data
            for i in range(len(filtered_tutors)):
                filtered_tutors[i] = ProfileSerializer(filtered_tutors[i]).data
            return JsonResponse({'filtered_tutors': filtered_tutors, 'course': course})
        return render(request, 'login/map.html', {'profile': request.user.profile, 'classes': classes})

@login_required
@transaction.atomic
def update_profile(request):
    classes = get_classes()
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
    classes = get_classes()
    school_data = get_schools()
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
        school_data = get_schools()
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

def get_schools():
    with open('staticfiles/login/class_sections.txt') as json_file:
        schools = json.load(json_file)
        return schools

def get_classes():
    with open('staticfiles/login/classes.txt') as json_file:
        data = json.load(json_file)
        return json.dumps(data)
