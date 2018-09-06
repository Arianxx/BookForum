from django.db.models.signals import post_save
from django.dispatch import receiver

from Discussion.models import DiscussReply, Notification


@receiver(post_save, sender=DiscussReply)
def send_notification(sender, instance, created, **kwargs):
    # todo: 发送通知
    if created:
        notify = Notification(sender=instance.user, instance=instance)
        notify.save()
        notify.receivers.set((instance.reply_to if len(instance.reply_to.all()) else []) + [instance.user])

    return True
