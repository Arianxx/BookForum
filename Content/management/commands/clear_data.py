from django.core.management import BaseCommand

from Content.models import Book, Auther, Tag, Publishing, Carousel
from Discussion.models import Discuss, DiscussReply
from User.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Carousel.objects.all().delete()
        DiscussReply.objects.all().delete()
        Discuss.objects.all().delete()
        Tag.objects.all().delete()
        Auther.objects.all().delete()
        Publishing.objects.all().delete()
        Book.objects.all().delete()
        User.objects.all().delete()

        print('Clear all the data.')