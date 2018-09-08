import random
from datetime import datetime

from django.conf import settings
from django.core.management import BaseCommand
from django.db.utils import IntegrityError
from faker import Faker

from Content.models import Book, Auther, Publishing, Tag
from Discussion.models import Discuss, DiscussReply
from User.models import User


class Command(BaseCommand):

    def handle(self, *arg, **kwargs):
        # fake = Faker("zh_CN")
        fake = Faker()
        try:
            fake_num = settings.PER_FAKE_BOOK_NUM
        except AttributeError:
            fake_num = 100

        for _ in range(fake_num):
            # 生成随机信息的用户
            try:
                user = User.objects.create_user(
                    username=fake.user_name(),
                    password='testtest',
                )
                user.first_name = fake.first_name()
                user.last_name = fake.last_name()
                user.email = fake.email()
                user.birth = datetime.strptime(fake.date(), '%Y-%m-%d')
                user.about = fake.text()
                user.link = fake.url()
                user.is_confirmed = True
                user.save()
                print('Fake user:', user.username)
            except IntegrityError:
                pass

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
            # 为书籍随机选择作者、出版社等
            auther = random.choice(all_authers)
            pub = random.choice(all_pubs)

            tags = []
            for _ in range(3):
                tag = random.choice(all_tags)
                tags.append(tag)

            try:
                book = Book(
                    name=''.join(fake.words()),
                    intro=fake.text() * 10,
                    publishing=pub,
                    auther=auther,
                    viewing=random.randint(0, 1000),
                )
                book.save()
                book.tags.add(*tags)
                book.save()

                print('Fake book: ', book)
            except IntegrityError:
                pass

        all_books = Book.objects.all()
        all_users = User.objects.all()
        for _ in range(fake_num):
            # 随机选择书籍生成讨论，并随机选择作者
            book = random.choice(all_books)
            user = random.choice(all_users)

            discuss = Discuss(
                title=''.join(fake.words()).capitalize(),
                body=fake.text() * 7,
                book=book,
                user=user,
            )

            discuss.save()

            for _ in range(random.randrange(10)):
                user = random.choice(all_users)
                mention_user = random.choice(all_users)
                try:
                    discuss_reply = DiscussReply(
                        body=fake.text() * 4 + ' @' + mention_user.username,
                        discuss=discuss,
                        user=user,
                    )
                except IndexError:
                    discuss_reply = DiscussReply(
                        body=fake.text() * 4 + ' @' + mention_user.username,
                        discuss=discuss,
                        user=user,
                    )
                discuss_reply.save()
                print('Fake reply: ', discuss_reply)

            print('Fake the discussion: ', discuss)
