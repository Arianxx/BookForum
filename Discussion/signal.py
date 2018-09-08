from django.db.models.signals import post_save

from Discussion.models import Discuss, DiscussReply, Notification


def send_notification(sender, instance, created, **kwargs):
    if len(instance.mentions.all()):
        if hasattr(instance, 'discuss'):
            notify = Notification(sender=instance.user, reply=instance, discuss=instance.discuss)
        else:
            notify = Notification(sender=instance.user, discuss=instance)
        notify.save()
        receivers = set(instance.mentions.all() if len(instance.mentions.all()) else [])
        notify.receivers.set(receivers)

    if hasattr(instance, 'discuss') and instance.user != instance.discuss.user:
        notify = Notification(sender=instance.user, reply=instance, is_reply=True)
        notify.save()
        receivers = [instance.discuss.user]
        notify.receivers.set(receivers)

    return True


post_save.connect(send_notification, sender=Discuss, dispatch_uid='discuss')
post_save.connect(send_notification, sender=DiscussReply, dispatch_uid='reply')