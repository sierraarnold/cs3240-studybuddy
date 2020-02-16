from django.contrib import admin
from .models import Profile, TutorCourse, StudentCourse

class CourseInlineTutor(admin.TabularInline):
    model = TutorCourse
    extra = 3

class CourseInlineStudent(admin.TabularInline):
    model = StudentCourse
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', ]}),
    ]
    inlines = [CourseInlineTutor, CourseInlineStudent]
    list_display = ('user', 'username', )
    search_fields = ['username']

class StudentCourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [field.name for field in StudentCourse._meta.get_fields()]}),
    ]
    list_display = [field.name for field in StudentCourse._meta.get_fields()]

class TutorCourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [field.name for field in TutorCourse._meta.get_fields()]}),
    ]
    list_display = [field.name for field in TutorCourse._meta.get_fields()]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
admin.site.register(TutorCourse, TutorCourseAdmin)
