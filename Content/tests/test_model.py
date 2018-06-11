from django.test import TestCase

from Discussion.models import (
    Discuss,
    DiscussReply,
)
from ..models import (
    Book,
    Auther,
    Publishing,
    Tag,
)


# Create your tests here.

class RelationshipTestCase(TestCase):
    """
    测试数据库关系是否正确
    """

    def setUp(self):
        auther = Auther.objects.create(name="Mike")
        pub = Publishing.objects.create(name="Test Publishing House")

        book = Book(name="Test Book")
        book.publishing = pub
        book.auther = auther
        book.save()

        self.book = book
        self.pub = pub
        self.auther = auther

    def test_book_basic(self):
        self.assertTrue(self.book.publishing_id == self.pub.id)
        self.assertTrue(self.book.auther_id == self.auther.id)

    def test_book_tag(self):
        tag = Tag.objects.create(name="Test")
        self.book.tags.add(tag)
        self.book.save()

        self.assertTrue(tag in self.book.tags.all())
        self.assertTrue(self.book in tag.books.all())

    def test_book_discuss(self):
        discuss = Discuss(title="Test Discuss")
        discuss.book = self.book
        discuss.save()

        self.assertTrue(discuss in self.book.discussions.all())
        self.assertTrue(discuss.book == self.book)

    def test_discuss_reply(self):
        discuss = Discuss.objects.create(title="Test Discuss", book=self.book)
        reply = DiscussReply.objects.create(discuss=discuss)

        self.true = self.assertTrue(reply.discuss == discuss)


class ImgTestCase(TestCase):

    def test_default_cover_path(self):
        auther = Auther(name='Test')
        auther.save()
        book = Book(name='Test Book', auther=auther)
        book.save()

        cover_path = book.cover.path
        default_path = book.cover.field.default.replace('/', '\\')

        self.assertTrue(default_path in cover_path)
