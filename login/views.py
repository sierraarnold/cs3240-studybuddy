from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from allauth.account.forms import LoginForm 

"""class MyCustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):
        # Add your own processing here.
        # You must return the original result.
        save_user(self, request, user, form)
        return super(MyCustomLoginForm, self).login(*args, **kwargs)"""

def home(request):
    template = loader.get_template('login/home.html')
    return render(request, 'login/home.html')

def index(request):
    extra_data = []
    if request.user.is_authenticated:
        extra_data = request.user.socialaccount_set.all()[0].extra_data
    return render(request, 'login/index.html', {'extra_data': extra_data})

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('login:home', args=()))


