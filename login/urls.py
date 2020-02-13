from django.urls import path
from . import views

app_name = "login"

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('logout', views.signout, name="signout"),
    path('departments', views.schools, name="schools"),
    path('courses', views.courses, name='courses'),
    path('departments/section', views.get_section, name='get_section'),
]
