from django.contrib import admin
from .models import Profile, TutorCourse, StudentCourse, MobileNotification, InAppMessage

class CourseInlineTutor(admin.TabularInline):
    model = TutorCourse
    extra = 3

class CourseInlineStudent(admin.TabularInline):
    model = StudentCourse
    extra = 3

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', 'phone_number', 'push_token', 'bio', 'year', 'location']}),
    ]
    inlines = [CourseInlineTutor, CourseInlineStudent]
    list_display = ('user', 'username', 'push_token')
    search_fields = ['username', 'phone_number',]

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

class MobileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [field.name for field in MobileNotification._meta.get_fields()]}),
    ]
    list_display = [field.name for field in MobileNotification._meta.get_fields()]

class InAppAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [field.name for field in InAppMessage._meta.get_fields()]}),
    ]
    list_display = [field.name for field in InAppMessage._meta.get_fields()]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
admin.site.register(TutorCourse, TutorCourseAdmin)
admin.site.register(MobileNotification, MobileAdmin)
admin.site.register(InAppMessage, InAppAdmin)
