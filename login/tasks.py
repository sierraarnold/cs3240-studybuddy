from .models import InAppMessage
from django.contrib.auth.models import User
from fcm_django.models import FCMDevice
from django.contrib import messages

#Creates a new InAppMessage with correct sender and recipient objects
def send_new_message_push_notification(**kwargs):
    sender = User.objects.get(id=kwargs.get("sender_id"))
    recipient = User.objects.get(id=kwargs.get("recipient_id"))
    request = sender.profile.first_name + " " + sender.profile.last_name + " has requested you as a tutor! Contact them via phone at " + sender.profile.phone_number + " or via email at " + sender.email
    notification = InAppMessage(recipient=recipient, sender=sender, title=kwargs.get("title"), message=request)
    notification.save()
    try:
        device = FCMDevice.objects.get(user=recipient)
        device.send_message(title=notification.title, body=notification.message)
    except:
        pass
