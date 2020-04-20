from rest_framework import serializers
from .models import Profile, TutorCourse, StudentCourse, InAppMessage
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

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    studentCourses = StudentCourseSerializer(many=True, source="studentcourse_set")
    tutorCourses = TutorCourseSerializer(many=True, source="tutorcourse_set")
    class Meta:
        depth = 1
        model = Profile
        fields = ( "first_name", "last_name", "username", 'phone_number', 'year','bio', 'location', "user", 'studentCourses', 'tutorCourses', 'email')

class InAppMessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(many=False, read_only=True)
    recipient = ProfileSerializer(many=False, read_only=True)
    class Meta:
        model = InAppMessage
        fields = [ 'message', 'status', 'sender', 'recipient', 'id', 'timestamp']
