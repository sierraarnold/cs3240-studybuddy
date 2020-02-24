from django.urls import path
from . import views

app_name = "login"

urlpatterns = [
    path('', views.renderTutorPage, name='home'),
    path('logout', views.signout, name="signout"),
    path('departments', views.schools, name="schools"),
    path('courses', views.courses, name='courses'),
    path('departments/section', views.get_section, name='get_section'),
    path('profile', views.update_profile, name='edit_profile'),
    path('notifications', views.notifications, name='notifications'),
    path('firebase-messaging-sw.js', views.ServiceWorkerView.as_view(), name='service_worker')
]
