from rest_framework import serializers
from .models import Profile, TutorCourse, StudentCourse, MobileNotification, InAppMessage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "id", "profile")

class TutorCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TutorCourse
        fields = [ 'name', 'dept', 'number']

class StudentCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentCourse
        fields = [ 'name', 'dept', 'number']

class MobileNotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(many=False, read_only=True, source="user_device_notifications")
    class Meta:
        model = MobileNotification
        fields = [ 'title', 'message', 'status', 'recipient', 'id']

class InAppMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)
    recipient = UserSerializer(many=False, read_only=True)
    class Meta:
        model = InAppMessage
        fields = [ 'title', 'message', 'status', 'sender', 'recipient', 'id']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    studentCourses = StudentCourseSerializer(many=True, source="studentcourse_set")
    tutorCourses = TutorCourseSerializer(many=True, source="tutorcourse_set")
    class Meta:
        depth = 1
        model = Profile
        fields = ( "username", 'phone_number', "user", 'studentCourses', 'tutorCourses')
