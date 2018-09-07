from django.db.models.signals import post_save
from django.dispatch import receiver

from Discussion.models import DiscussReply, Notification


@receiver(post_save, sender=DiscussReply)
def send_notification(sender, instance, created, **kwargs):
    if len(instance.reply_to.all()):
        notify = Notification(sender=instance.user, instance=instance)
        notify.save()
        receivers = set(instance.reply_to.all() if len(instance.reply_to.all()) else [])
        notify.receivers.set(receivers)

    if instance.user != instance.discuss.user:
        notify = Notification(sender=instance.user, instance=instance, is_reply=True)
        notify.save()
        receivers = [instance.discuss.user]
        notify.receivers.set(receivers)

    return True
