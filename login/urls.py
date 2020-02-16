from django.urls import path
from . import views

app_name = "login"

urlpatterns = [
    path('', views.tutor, name='home'),
    path('logout', views.signout, name="signout"),
    path('departments', views.schools, name="schools"),
    path('courses', views.courses, name='courses'),
    path('departments/section', views.get_section, name='get_section'),
    path('profile', views.update_profile, name='edit_profile'),
]
