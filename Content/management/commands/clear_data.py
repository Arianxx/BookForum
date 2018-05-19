from django.core.management import BaseCommand
from Content.models import Book, Auther, Tag, Publishing, Discuss, DiscussReply, Poll

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Poll.objects.all().delete()
        DiscussReply.objects.all().delete()
        Discuss.objects.all().delete()
        Poll.objects.all().delete()
        Tag.objects.all().delete()
        Auther.objects.all().delete()
        Publishing.objects.all().delete()
        Book.objects.all().delete()

        print('Clear all the data.')