from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from django.http import HttpResponse
from django.dispatch import receiver
from django.shortcuts import redirect
from django.conf import settings


class MyLoginAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.user.is_authenticated:
            return settings.LOGIN_REDIRECT_URL.format(id=request.user.id)
        else:
            return "/"


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        pass    # TODOFuture: To perform some actions right after successful login

    def is_open_for_signup(self, request, sociallogin):
        if sociallogin.user.email != "virginia.edu":
            return False
        return super(SocialAccountAdapter, self).is_open_for_signup(request, sociallogin)

@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    email_address = sociallogin.account.extra_data['email']
    User = get_user_model()
    users = User.objects.filter(email=email_address)
    if users:
        perform_login(request, users[0], email_verification='optional')
        raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL.format(id=request.user.id)))
