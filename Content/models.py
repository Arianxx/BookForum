from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify


# Create your models here.

class Book(models.Model):
    """
    它和计票模型（Poll）是一对一关系。这个关系在Poll模型中定义，因为书籍id是计票模型的外键，以便删除时的一致性。因此不会存在没有引用书籍的计
    票模型对象。
    它还和讨论模型（Discuss)拥有一对多关系。
    """
    # TODO: 增加查看次数信息
    name = models.CharField(max_length=32, verbose_name="book name")
    pub_date = models.DateField(default=timezone.now, blank=True, null=True)
    slug = models.SlugField(max_length=64, unique=True)
    intro = models.TextField(max_length=1280, blank=True)

    publishing = models.ForeignKey("Publishing", on_delete=models.CASCADE, related_name="books", null=True)
    auther = models.ForeignKey("Auther", on_delete=models.CASCADE, related_name="books")
    tags = models.ManyToManyField("Tag", related_name="books")

    class Meta:
        ordering = ['pub_date']
        unique_together = ['name', 'auther', ]

    def __str__(self):
        return "Book(%s)" % self.name

    def save(self, *args, **kwargs):
        # 自动根据书籍的名称和作者添加一个slug
        slug = ' writen by '.join([self.name, self.auther.name])
        self.slug = slugify(slug)

        ret = super(Book, self).save(*args, **kwargs)

        # 保存书籍时，一并保存它的计票对象（Poll），从而不用手动去创建计票对象。
        try:
            self.__getattribute__("poll")
        except AttributeError:
            poll = Poll(book=self)
            poll.save()

        return ret


class Auther(models.Model):
    """
    与书籍模型（Book）是一对一关系。关系在Book中定义。
    """
    name = models.CharField(max_length=32, verbose_name="auther name")
    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return "Auther(%s)" % self.name


class Publishing(models.Model):
    """
    与书籍模型（Book）是一对一关系。关系在Book中定义。
    """
    name = models.CharField(max_length=32, verbose_name="publishing name")

    def __str__(self):
        return "Publishing(%s)" % self.name


class Tag(models.Model):
    """
    与书籍模型（Book)是多对多关系。关系在Book中定义。
    """
    name = models.CharField(max_length=32, verbose_name="tag name", unique=True)

    def __str__(self):
        return "Tag(%s)" % self.name


class Poll(models.Model):
    """
    计票模型。保存了赞同和反对的信息。
    """
    # TODO:使用django内置的user对象来投票，并记录投票人。
    up = models.IntegerField(default=0, verbose_name="up's count")
    down = models.IntegerField(default=0, verbose_name="down's count")
    book = models.OneToOneField("Book", on_delete=models.CASCADE)

    def __str__(self):
        return "Poll(book:%s, up:%d, down:%d)" % (self.book.name, self.up, self.down)


class Discuss(models.Model):
    """
    关于这本书籍的讨论。
    它和讨论回复模型（DiscussReply）拥有一对多关系。
    """
    # TODO:关联user对象。
    title = models.CharField(max_length=128, verbose_name="discussion title")
    body = models.TextField(max_length=1280, blank=True, verbose_name="discussion")
    pub_date = models.DateField(default=timezone.now, blank=True, null=True)

    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="discussions")

    def __str__(self):
        return "Discuss(book='%s', title='%s')" % (self.book.name, self.title)


class DiscussReply(models.Model):
    """
    讨论的回复。
    """
    # TODO:关联user对象。消息提醒。
    body = models.TextField(max_length=1280, verbose_name="reply")
    pub_date = models.DateField(default=timezone.now, blank=True, null=True)

    discuss = models.ForeignKey("Discuss", on_delete=models.CASCADE, related_name="replys")

    def __str__(self):
        return "DiscussReply(Discuss title='%s')" % self.discuss.title
