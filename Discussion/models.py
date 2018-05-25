from django.db import models
from django.utils import timezone

from Content.models import Book
from .exceptions import DeepReplyError, IsolateReplyError


# Create your models here.

class Discuss(models.Model):
    """
    关于这本书籍的讨论。
    它和讨论回复模型（DiscussReply）拥有一对多关系。
    """
    # TODO:关联user对象。,
    title = models.CharField('讨论标题', max_length=128)
    body = models.TextField('讨论正文', max_length=1280, blank=True)
    pub_date = models.DateField(default=timezone.now, blank=True, null=True)

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="discussions")

    class Meta:
        verbose_name = '书籍讨论'
        verbose_name_plural = '书籍讨论'

    def __str__(self):
        return "Discuss(book='%s', title='%s')" % (self.book.name, self.title)


class DiscussReply(models.Model):
    """
    讨论的回复。
    回复可以分为两个层级。第一个为直接回复讨论（Discuss）的父评论，第二个为回复评论本身的子评论。
    每个评论可以拥有一个reply_to字段，表明它是否是回复另一个评论的评论。
    """
    # TODO:关联user对象。消息提醒。
    body = models.TextField('回复正文', max_length=1280)
    pub_date = models.DateField(default=timezone.now, blank=True, null=True)

    discuss = models.ForeignKey("Discuss", on_delete=models.CASCADE, related_name="replys")
    parent_reply = models.ForeignKey('DiscussReply', on_delete=models.CASCADE, related_name='sub_replys', null=True)
    reply_to = models.ForeignKey('DiscussReply', on_delete=models.CASCADE, related_name='replys', null=True)

    class Meta:
        verbose_name = '讨论回复'
        verbose_name_plural = '讨论回复'

    def __str__(self):
        return "DiscussReply(Discuss title='%s')" % self.discuss.title

    def save(self, *args, **kwargs):
        if self.parent_reply:
            if self.parent_reply.parent_reply:
                # 将子评论限制在两层
                raise DeepReplyError("Can't reply to another sub reply!")

        if self.reply_to and not self.parent_reply:
            # 如果这个评论指向了另一个评论，却又是一个父评论，就弹出错误。父评论不能指向任何评论。
            raise IsolateReplyError("Can't make a isolate reply!")

        return super().save(*args, **kwargs)
