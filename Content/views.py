from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Book, Discuss
from django.conf import settings

# Create your views here.

class IndexView(generic.ListView):
    model = Book
    context_object_name = 'Books'
    template_name = 'Content/index.html'
    paginate_by = getattr(settings,'PER_PAGE_SHOW', 20)
    paginate_orphans = getattr(settings,'ORPHANS_PAGE_SHOW', 5)

    def get_ordering(self):
        sort = self.kwargs.get('sort', '-pub_date')
        return (str(sort), '-pub_date', '-id')

class DiscussView(generic.ListView):
    model = Discuss
    context_object_name = 'Discussions'
    template_name = 'Content/discussions.html'
    paginate_by = getattr(settings, 'PER_PAGE_SHOW', 20)
    paginate_orphans = getattr(settings, 'ORPHANS_PAGE_SHOW', 5)

    def get_ordering(self):
        sort = self.kwargs.get('sort', '-pub_date')
        return (str(sort), '-pub_date', '-id')