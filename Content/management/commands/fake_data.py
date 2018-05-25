import random
from datetime import datetime

from django.conf import settings
from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from faker import Faker

from Content.models import Book, Auther, Publishing, Tag
from Discussion.models import Discuss, DiscussReply


class Command(BaseCommand):

    def handle(self, *arg, **kwargs):
        fake = Faker()
        try:
            fake_num = settings.PER_FAKE_BOOK_NUM
        except AttributeError:
            fake_num = 100

        for _ in range(fake_num // 10):
            # 生成一本书的基本信息，如作者、出版社等
            try:
                auther = Auther(
                    name=fake.name(),
                    about='. '.join([fake.text() for _ in range(10)]),
                )
                auther.save()

                publishing = Publishing(
                    name=fake.company(),
                    about='. '.join([fake.text() for _ in range(10)]),
                    establish_date=datetime.utcfromtimestamp(fake.unix_time()),
                )
                publishing.save()

                tag = Tag(
                    name=fake.word()
                )
                tag.save()
            except IntegrityError:
                # 忽略生成相同的键所造成的错误
                pass

        all_authers = Auther.objects.all()
        all_tags = Tag.objects.all()
        all_pubs = Publishing.objects.all()
        for _ in range(fake_num):
            #为书籍随机选择作者、出版社等
            auther = random.choice(all_authers)
            pub = random.choice(all_pubs)

            tags = []
            for _ in range(3):
                tag = random.choice(all_tags)
                tags.append(tag)

            book = Book(
                name=' '.join(fake.words()),
                intro=fake.text() * 10,
                publishing=pub,
                auther=auther
            )
            book.save()
            poll = book.poll
            poll.up = fake.random_digit()
            poll.down = fake.random_digit()
            poll.save()
            book.tags.add(*tags)
            book.save()

            print('Fake book: ', book)

        all_books = Book.objects.all()
        for _ in range(fake_num * 10):
            #随机选择书籍生成讨论
            book = random.choice(all_books)

            discuss = Discuss(
                title=' '.join(fake.words()).capitalize(),
                body=fake.text() * 7,
                book=book,
            )

            discuss.save()

            for _ in range(random.randrange(fake_num // 10)):
                discuss_reply = DiscussReply(
                    body=fake.text() * 4,
                    discuss=discuss
                )
                discuss_reply.save()

            print('Fake the discussion: ', discuss)
