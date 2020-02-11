from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def index(request):
    extra_data = []
    if request.user.is_authenticated:
        extra_data = request.user.socialaccount_set.all()[0].extra_data
    return render(request, 'login/index.html', {'extra_data': extra_data})

def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('login:index', args=()))
