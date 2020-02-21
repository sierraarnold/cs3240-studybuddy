from .models import Profile, MobileNotification
from django.contrib.auth.models import User
from fcm_django.models import FCMDevice

def send_new_message_push_notification(**kwargs):
    sender = User.objects.get(id=kwargs.get("sender_id"))
    recipient = User.objects.get(id=kwargs.get("recipient_id"))
    content = kwargs.get("content")
    notification = MobileNotification()
    notification.recipient = recipient
    notification.title = "New notification"
    sender_full_name = "{} {}".format(sender.first_name,
                                      sender.last_name)
    message = '{} has sent you a message: "{}"'.format(sender_full_name,
                                                       content)
    notification.message = message
    notification.save()

    device = FCMDevice.objects.get(user=recipient)
    device.send_message(notification.tile, message)
