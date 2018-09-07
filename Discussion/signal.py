from django.db.models.signals import post_save

from Discussion.models import DiscussReply, Notification


def send_notification(sender, instance, created, **kwargs):
    if created:
        if len(instance.reply_to.all()):
            notify = Notification(sender=instance.user, instance=instance)
            notify.save()
            receivers = set(instance.reply_to if len(instance.reply_to.all()) else [])
            try:
                receivers.remove(instance.user)
            except KeyError:
                pass
            notify.receivers.set(receivers)

        if instance.user != instance.discuss.user:
            notify = Notification(sender=instance.user, instance=instance)
            notify.save()
            receivers = [instance.discuss.user]
            notify.receivers.set(receivers)

    return True


post_save.connect(send_notification, sender=DiscussReply)
