from django.core.management import BaseCommand
from django.conf import settings
from django.db.utils import IntegrityError
from faker import Faker
import random
from Content.models import Book, Auther, Publishing, Tag, Poll, Discuss, DiscussReply

class Command(BaseCommand):

    def handle(self, *arg, **kwargs):
        fake = Faker()
        try:
            fake_num = settings.PER_FAKE_BOOK_NUM
        except AttributeError:
            fake_num = 100

        for _ in range(fake_num//10):
            try:
                auther = Auther(
                    name = fake.name(),
                    age = fake.random_digit(),
                    location = fake.address()
                )
                auther.save()

                publishing = Publishing(
                    name = fake.company()
                )
                publishing.save()

                tag = Tag(
                    name = fake.word()
                )
                tag.save()
            except IntegrityError:
                pass

        all_authers = Auther.objects.all()
        all_tags = Tag.objects.all()
        all_pubs = Publishing.objects.all()
        for _ in range(fake_num):
            auther = random.choice(all_authers)
            pub = random.choice(all_pubs)

            tags = []
            for _ in range(3):
                tag = random.choice(all_tags)
                tags.append(tag)

            book = Book(
                name = ' '.join(fake.words()),
                intro = fake.text() * 10,
                publishing = pub,
                auther = auther
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
        for _ in range(fake_num):
            book = random.choice(all_books)

            discuss = Discuss(
                title = ' '.join(fake.words()).capitalize(),
                body = fake.text() * 7,
                book = book,
            )

            discuss.save()

            for _ in range(random.randrange(fake_num//10)):
                discuss_reply = DiscussReply(
                    body = fake.text() * 4,
                    discuss = discuss
                )
                discuss_reply.save()

            print('Fake the discussion: ', discuss)
