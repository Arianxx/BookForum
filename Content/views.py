from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Book, Poll, Tag, Auther, Publishing


# Create your views here.

class IndexView(generic.ListView):
    model = Book
    context_object_name = 'Books'
    template_name = 'Content/index.html'
    paginate_by = getattr(settings, 'PER_PAGE_SHOW', 20)
    paginate_orphans = getattr(settings, 'ORPHANS_PAGE_SHOW', 5)

    def get_ordering(self):
        sort = self.kwargs.get('sort', '-pub_date')
        return str(sort), '-pub_date', '-id'


class TagView(generic.ListView):
    model = Book
    content_object_name = 'Books'
    template_name = 'Content/tag_books.html'
    paginate_by = getattr(settings, 'PER_PAGE_SHOW', 20)
    paginate_orphans = getattr(settings, 'ORPHANS_PAGE_SHOW', 5)

    def get_ordering(self):
        sort = self.kwargs.get('sort', '-pub_date')
        return str(sort), '-pub_date', '-id'

    def get_queryset(self):
        query_set = super().get_queryset()
        slug = self.kwargs.get('slug')
        tag = get_object_or_404(Tag, slug=slug)
        return query_set.filter(tags=tag)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs.get('slug')
        tag = get_object_or_404(Tag, slug=slug)
        context['tag'] = tag
        return context


class AutherView(generic.ListView):
    model = Book
    context_object_name = 'Books'
    template_name = 'Content/auther_books.html'
    paginate_by = getattr(settings, 'PER_PAGE_SHOW', 20)
    paginate_orphans = getattr(settings, 'ORPHANS_PAGE_SHOW', 5)

    def get_ordering(self):
        sort = self.kwargs.get('sort', '-pub_date')
        return str(sort), '-pub_date', '-id'

    def get_queryset(self):
        query_set = super().get_queryset()
        slug = self.kwargs.get('slug')
        auther = get_object_or_404(Auther, slug=slug)
        return query_set.filter(auther=auther)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        slug = self.kwargs.get('slug')
        auther = get_object_or_404(Auther, slug=slug)
        context['auther'] = auther
        return context


class PublishingView(generic.ListView):
    model = Book
    context_object_name = 'Books'
    template_name = 'Content/publishing_books.html'
    paginate_by = getattr(settings, 'PER_PAGE_SHOW', 20)
    paginate_orphans = getattr(settings, 'ORPHANS_PAGE_SHOW', 5)

    def get_queryset(self):
        query_set = super().get_queryset()
        slug = self.kwargs.get('slug')
        publishing = get_object_or_404(Publishing, slug=slug)
        return query_set.filter(publishing=publishing)

    def get_ordering(self):
        sort = self.kwargs.get('sort', '-pub_date')
        return str(sort), '-pub_date', '-id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs.get('slug')
        publishing = get_object_or_404(Publishing, slug=slug)
        context['publishing'] = publishing
        return context


class BookView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'Content/book_detail.html'

    def get_context_data(self, **kwargs):
        # 从session里获取暂存的表单信息，获取后就将其删除
        context = super().get_context_data(**kwargs)
        form = self.request.session.get('DiscussionForm')
        context['form'] = form
        self.request.session['DiscussionForm'] = None
        return context


def all_hot_books(request):
    # TODO：更好的计算方式
    polls = Poll.objects.order_by('-up').all()[:10]
    books = [poll.book for poll in polls]
    context = {
        'books': books,
    }
    return render(request, 'Content/hot_books.html', context=context)
