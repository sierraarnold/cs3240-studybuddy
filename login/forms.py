"""
/***************************************************************************************
*  REFERENCES
*  Title: How to Extend Django User Model
*  Author: N/A
*  Date: 4/27/20
*  Code version: N/A
*  URL: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
*  Software License: N/A
**************************************************************************************/
"""
from django import forms
from .models import Profile, StudentCourse, TutorCourse
from django.contrib.auth.models import User
import json

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_courses = list(StudentCourse.objects.filter(user=self.instance.id).values())
        self.tutor_courses = list(TutorCourse.objects.filter(user=self.instance.id).values())
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'year', 'bio')
