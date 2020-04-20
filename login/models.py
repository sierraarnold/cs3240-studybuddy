from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    username = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30, default="")
    year = models.CharField(max_length=10, default="")
    bio = models.CharField(max_length=300, default="")
    push_token = models.CharField(max_length=200)
    location = models.CharField(max_length=50, default="Inactive")
    email = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.username

class TutorCourse(models.Model):
    name = models.CharField(max_length=200)
    dept = models.CharField(max_length=200)
    number = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class StudentCourse(models.Model):
    name = models.CharField(max_length=200)
    dept = models.CharField(max_length=200)
    number = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class InAppMessage(models.Model):
    sender = models.ForeignKey(Profile, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, default='unread')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
