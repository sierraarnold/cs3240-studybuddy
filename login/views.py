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
from .models import Profile, StudentCourse, TutorCourse, MobileNotification, InAppMessage
from login.serializers import ProfileSerializer, StudentCourseSerializer, TutorCourseSerializer, MobileNotificationSerializer, InAppMessageSerializer
from .tasks import send_new_message_push_notification

# Simple signout function using Django's authentication
def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Signed out')
        return HttpResponseRedirect(reverse('login:home', args=()))

"""
    If not authenticated:
        render default page without search capabilities
    Else:
        Get all courses from the course text file
        Get profile data from user object
        Update messages badge count by getting all sent to user and checking read status
        If post request:
            Handle post request
            return JsonResponse containing:
                User's profile object
                filtered tutors (if filtering by all student courses)
                desired tutor to send notification to (if requesting)
                the course filtered by (if filtering by course)
        Else:
            render template passing user's profile and all UVA courses

    Handling the post request involves processing data from post request:
            Was a list of courses passed? - User is filtering by all of their student courses:
                Need to filter profiles by associated tutorcourses in this list
            Was a course object passed? - User is filtering by a specific course:
                Need to filter profiles by associated tutorcourses that are this course
            Was a pushtoken passed? - User's pushtoken needs to be refreshed:
                Need to save user's profile's pushtoken
                Need to update FCMDevice associated with profile
            The last option is if user pressed request button:
                Need to send_new_message_push_notification. See tasks.py
"""
def renderTutorPage(request):
    if not request.user.is_authenticated:
        return render(request, 'login/tutorSearch.html')
    else:
        classes = get_classes_fromtxt()
        profile = json.dumps(ProfileSerializer(request.user.profile).data)
        filtered_tutors = []
        getNotifications(request)
        if request.method == 'POST' and request.is_ajax():
            course = request.POST.get('course', "")
            courses = json.loads(request.POST.get('courses', '[]'))
            pushToken_registration = json.loads(request.POST.get('pushToken_registration', '{}'))
            tutor = json.loads(request.POST.get('tutor', '{}'))
            library = request.POST.get('library', "")
            startTutoringAt = request.POST.get('startTutoringAt', "")
            if len(courses) > 0:
                course_names = []
                for class_ in courses:
                    course_names.append(class_['name'])
                filtered_tutors = list(Profile.objects.filter(tutorcourse__name__in=course_names))
            elif course != "":
                course = course.split('-')[1].lstrip()
                filtered_tutors = list(Profile.objects.filter(tutorcourse__name=course))
            elif library != "":
                filtered_tutors = list(Profile.objects.filter(location=library))
            elif startTutoringAt != "":
                user_profile = Profile.objects.get(id = request.user.profile.id)
                if user_profile.location == startTutoringAt:
                    startTutoringAt = "Not tutoring"
                user_profile.location = startTutoringAt
                user_profile.save()
                return JsonResponse({'libraryAdded': user_profile.location})
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
                return JsonResponse({'registration_id': pushToken_registration['registration_id'], 'type': pushToken_registration['type'], 'profile': profile})
            elif bool(tutor):
                send_new_message_push_notification(sender_id=request.user.id, recipient_id=tutor['user']['id'], title="Message from " + request.user.email, message="Tutor request")
            for i in range(len(filtered_tutors)):
                filtered_tutors[i] = ProfileSerializer(filtered_tutors[i]).data

            return JsonResponse({'profile': profile, 'filtered_tutors': filtered_tutors, 'tutor':tutor, 'course': course})
        return render(request, 'login/tutorSearch.html', {'profile': profile, 'classes': classes})

"""
    Get all UVA courses
    If saving profile, hence a POST request is recieved:
        Save courses
        Process user form and profile form to see if valid
        If valid:
            Save forms, which automatically update user and profile objects
            Redirect to home
        Else:
            Show error message
    Else:
        Just display user form and profile form, passing in all UVA courses

"""
@login_required
@transaction.atomic
def update_profile(request):
    classes = get_classes_fromtxt()
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            saveClasses(request.POST.items(), request.user.profile.id)
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
    TutorCourse.objects.filter(user_id=user_id).delete()
    StudentCourse.objects.filter(user_id=user_id).delete()
    for key, value in postedItems:
        if value == "course":
            if(key.startswith('Tutor')):
                (dept, number, name) = parseCourse(key)
                tutor_course = TutorCourse(dept=dept, number=number, name=name, user_id=user_id)
                tutor_course.save()
            if(key.startswith('Student')):
                (dept, number, name) = parseCourse(key)
                student_course = StudentCourse(dept=dept, number=number, name=name, user_id=user_id)
                student_course.save()

"""
    Gets all notifications - all sent by user and recieved
    Sets notification count of unread recieved messages in session
    Returns json object of all notifications
"""
def getNotifications(request):
    inappmessages = list(InAppMessage.objects.filter(sender=request.user.id))
    inappmessages += list(InAppMessage.objects.filter(recipient=request.user.id))
    mobilenotifications = list(MobileNotification.objects.filter(recipient=request.user.id))
    for i in range(len(inappmessages)):
        inappmessages[i] = InAppMessageSerializer(inappmessages[i]).data
        inappmessages[i]['recipient'] = dict(inappmessages[i]['recipient'])
        inappmessages[i]['sender'] = dict(inappmessages[i]['sender'])
    for i in range(len(mobilenotifications)):
        mobilenotifications[i] = MobileNotificationSerializer(mobilenotifications[i]).data
        mobilenotifications[i]['recipient'] = dict(mobilenotifications[i]['recipient'])
    all_notifications = mobilenotifications + inappmessages
    notificationCount = 0
    for notification in all_notifications:
        if notification['status'] == 'unread' and notification['recipient']['id'] == request.user.id:
            notificationCount += 1
    request.session['notificationCount'] = notificationCount
    return (json.dumps(all_notifications))

"""
    Gets all notifications
    For every notification in all notifications:
        If unread and is a recieved message:
            Mark as read
    Set notificationcount in session to 0
    Render notificationlist
"""
@login_required
def notifications(request):
    all_notifications = getNotifications(request)
    notificationList = json.loads(all_notifications)
    for notification in notificationList:
        if notification['status'] == 'unread' and notification['recipient']['id'] == request.user.id:
            if notification['sender']:
                message = InAppMessage.objects.get(id=notification['id'])
                message.status = 'read'
                message.save()
            else:
                message = MobileNotification.objects.get(id=notification['id'])
                message.status = 'read'
                message.save()
    request.session['notificationCount'] = 0
    return render(request, 'login/notifications.html', {'all_notifications': all_notifications})

# This class is needed for the server to find the service worker file to run js in background
class ServiceWorkerView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login/firebase-messaging-sw.js', content_type="application/x-javascript")

"""
    Returns a tuple all all parts of checkbox course formatted as Tutor:{coursename}
    where {coursename} is formatted as {dept} {number} - {name}
"""
def parseCourse(course_name):
    course = course_name.split(':')[1]
    parts = course.split('-')
    dept_number = parts[0].rstrip()
    name = parts[1].lstrip()
    dept_parts = dept_number.split(' ')
    dept = dept_parts[0]
    number = dept_parts[1]
    return (dept, number, name)

#Renders departments page. where a department is like Arts and Sciences
def departments(request):
    classes = get_classes_fromtxt()
    department_data = get_departments_fromtxt()
    department_list = list(department_data.keys())
    department_section_list = list(department_data.values())
    return render(request, 'login/departments.html', {'department_list': department_list, 'department_section_list': department_section_list, 'classes': classes})

#Renders courses page for a section of a department where a department is like Arts and Sciences, section is like CS and courses is like CS 2150...
def courses(request):
    courses = request.session['courses']
    if request.method == 'POST' and request.is_ajax():
        type = request.POST.get('type', "")
        course = request.POST.get('course', "").lstrip().rstrip()
        if course != "":
            (dept, number, name) = parseCourse("Tutor:" + course)
            if type == "Student":
                alreadyAdded = list(Profile.objects.filter(studentcourse__name=name))
                if len(alreadyAdded) == 0:
                    student_course = StudentCourse(dept=dept, number=number, name=name, user_id=request.user.id)
                    student_course.save()
                    return JsonResponse({'course': course})
                else:
                    return JsonResponse({'alreadyAdded': True})
            elif type == "Tutor":
                alreadyAdded = list(Profile.objects.filter(tutorcourse__name=name))
                if len(alreadyAdded) == 0:
                    tutor_course = TutorCourse(dept=dept, number=number, name=name, user_id=request.user.id)
                    tutor_course.save()
                    return JsonResponse({'course': course})
                else:
                    return JsonResponse({'alreadyAdded': True})
    return render(request, 'login/courses.html', {'courses':courses})

# Gets all courses of a section, where a section is like CS and courses are like CS 2150...
def get_department_section(request):
    try:
        courses = []
        link = request.POST['choice']
        courses = get_courses(link)
        request.session['courses'] = json.dumps(courses)
    except:
        messages.error(request, 'Cannot get courses at this time')
        return HttpResponseRedirect(reverse('login:departments'))
    return HttpResponseRedirect(reverse('login:courses'))

#Gets courses for a section by parsing Lou's list page for that section
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

def get_departments_fromtxt():
    with open('staticfiles/login/class_sections.txt') as json_file:
        return json.load(json_file)

def get_classes_fromtxt():
    with open('staticfiles/login/classes.txt') as json_file:
        data = json.load(json_file)
        return json.dumps(data)
