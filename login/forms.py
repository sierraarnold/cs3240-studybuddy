from django import forms
from .models import Profile, StudentCourse, TutorCourse
from django.contrib.auth.models import User
import json

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = self.instance.email
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_courses = list(StudentCourse.objects.filter(user=self.instance.id).values())
        self.tutor_courses = list(TutorCourse.objects.filter(user=self.instance.id).values())
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Profile
        fields = ('username', 'phone_number')    #, 'year', 'bio')
