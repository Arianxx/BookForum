from django.db import models
from django.utils import timezone

from Content.models import Book
from User.models import User


# Create your models here.

class Discuss(models.Model):
    """
    关于这本书籍的讨论。
    它和讨论回复模型（DiscussReply）拥有一对多关系。
    """
    title = models.CharField('讨论标题', max_length=128)
    body = models.TextField('讨论正文', max_length=1280, blank=True)
    pub_date = models.DateField(default=timezone.now, blank=True, null=True)

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="discussions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discussions")

    mentions = models.ManyToManyField(User, related_name='replys_from_discussion')

    class Meta:
        verbose_name = '书籍讨论'
        verbose_name_plural = '书籍讨论'

    def __str__(self):
        return "Discuss(book='%s', title='%s')" % (self.book.name, self.title)


class DiscussReply(models.Model):
    """
    讨论的回复。
    每个评论可以拥有一个reply_to字段，表明它是否是回复另一个评论的评论。
    """
    body = models.TextField('回复正文', max_length=1280)
    pub_date = models.DateField(default=timezone.now, blank=True, null=True)

    discuss = models.ForeignKey("Discuss", on_delete=models.CASCADE, related_name="replys")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replys')

    mentions = models.ManyToManyField(User, related_name='replys_from_reply')

    class Meta:
        verbose_name = '讨论回复'
        verbose_name_plural = '讨论回复'

    def __str__(self):
        return "DiscussReply(Discuss title='%s')" % self.discuss.title


class Notification(models.Model):
    """
    储存通知。
    绑定signal，当DiscussReply保存之后自动在此模型中存入相关信息
    """
    sender = models.ForeignKey(User, verbose_name='发送者', on_delete=models.CASCADE, related_name='sender_notifies')
    receiver = models.ForeignKey(User, verbose_name='接收者', on_delete=models.CASCADE, related_name='receive_notifies')
    discuss = models.ForeignKey(Discuss, verbose_name='主题', on_delete=models.CASCADE, related_name='notifies')
    reply = models.ForeignKey(DiscussReply, verbose_name='回复', on_delete=models.CASCADE, related_name='notifies',
                              null=True, blank=True)
    create_time = models.DateTimeField('创建日期', default=timezone.now, blank=True, null=True)
    is_read = models.BooleanField('是否阅读', default=False)
    # 通知分@和回复
    is_reply = models.BooleanField('是否是回复', default=False)

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ('-create_time',)

    def __str__(self):
        return "DiscussReply(Notification sender='%s')" % self.sender.username

    def mark_to_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()
