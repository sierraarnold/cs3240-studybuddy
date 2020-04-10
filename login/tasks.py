from .models import InAppMessage
from django.contrib.auth.models import User
from fcm_django.models import FCMDevice
from django.contrib import messages

#Creates a new InAppMessage with correct sender and recipient objects
def send_new_message_push_notification(**kwargs):
    sender = User.objects.get(id=kwargs.get("sender_id"))
    recipient = User.objects.get(id=kwargs.get("recipient_id"))
    notification = InAppMessage(recipient=recipient, sender=sender, title=kwargs.get("title"), message=sender.email + " has requested you as a tutor!")
    notification.save()
    try:
        device = FCMDevice.objects.get(user=recipient)
        device.send_message(title=notification.title, body=notification.message)
    except:
        pass
