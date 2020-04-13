from .models import InAppMessage, Profile
from fcm_django.models import FCMDevice
from django.contrib import messages

#Creates a new InAppMessage with correct sender and recipient objects
def send_new_message_push_notification(**kwargs):
    sender = Profile.objects.get(id=kwargs.get("sender_id"))
    recipient = Profile.objects.get(id=kwargs.get("recipient_id"))
    request = kwargs.get("message")
    notification = InAppMessage(recipient=recipient, sender=sender, title=request, message=request)
    notification.save()
    try:
        device = FCMDevice.objects.get(user=recipient)
        device.send_message(title=notification.title, body=notification.message)
    except:
        pass
