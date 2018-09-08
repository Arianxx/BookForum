from django.test import TestCase

from Content.models import Book, Auther
from ..exceptions import DeepReplyError, IsolateReplyError
from ..models import Discuss, DiscussReply


class DicussReplyTest(TestCase):

    def setUp(self):
        auther = Auther(name='Test')
        auther.save()
        book = Book(name='Test Book', auther=auther)
        book.save()

        self.discussion = Discuss(book=book, title='Test Discussion')
        self.discussion.save()

        replys = []
        for i in range(2):
            replys.append(DiscussReply(body='Test', discuss=self.discussion))
            replys[i].save()

        replys[1].parent_reply = replys[0]
        replys[1].save()
        self.replys = replys

    def test_deep_reply_error(self):
        deepest_reply = DiscussReply(body='Test', discuss=self.discussion)
        deepest_reply.parent_reply = self.replys[1]

        with self.assertRaises(DeepReplyError):
            deepest_reply.save()

    def test_isolate_reply_error(self):
        isolate_reply = DiscussReply(body='Test', discuss=self.discussion)
        isolate_reply.mentions = self.replys[0]

        with self.assertRaises(IsolateReplyError):
            isolate_reply.save()
