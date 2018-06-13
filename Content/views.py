import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic

from .forms import AddNodeForm, AddAutherForm, AddPublishingForm, AddTagForm
from .models import Book, Tag, Auther, Publishing


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

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        session = self.request.session
        # 每隔半小时访问，增加这本书的viewing次数
        key = 'book_{id}'.format(id=object.id)
        if not key in session:
            object.add_viewing()
            object.save()
            session[key] = time.time()
        else:
            now = time.time()
            if now - session[key] > 30 * 60:
                object.add_viewing()
                object.save()
                session[key] = time.time()
        return object


def all_hot_books(request):
    books = Book.objects.order_by('-viewing').all()[:10]
    context = {
        'books': books,
    }
    return render(request, 'Content/hot_books.html', context=context)


@login_required
def add_node(request):
    if request.method == 'POST':
        form = AddNodeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            messages.success(request, "成功增加节点")
            slug = form.instance.slug
            redirect_url = reverse('Content:book', kwargs={'slug': slug})
            return redirect(redirect_url)
    else:
        form = AddNodeForm()

    context = {
        'form': form,
    }
    return render(request, 'Content/add_node.html', context=context)


@login_required
def add_auther(request):
    if request.method == 'POST':
        form = AddAutherForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, '成功添加了一个作者，现在可以为其增添书籍')
            redirect_url = reverse('Content:add_node')
            return redirect(redirect_url)
    else:
        form = AddAutherForm()

    context = {
        'form': form,
    }
    return render(request, 'Content/add_auther.html', context=context)


@login_required
def add_publishing(request):
    if request.method == 'POST':
        form = AddPublishingForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, '你成功添加了一个出版社，现在可以为其增添书籍')
            redirect_url = reverse('Content:add_node')
            return redirect(redirect_url)
    else:
        form = AddPublishingForm()

    context = {
        'form': form
    }
    return render(request, 'Content/add_publishing.html', context=context)


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = AddTagForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, '你成功添加了一个tag，现在可以用其添加书籍')
            redirect_url = reverse('Content:add_node')
            return redirect(redirect_url)
    else:
        form = AddTagForm()

    context = {
        'form': form,
    }
    return render(request, 'Content/add_tag.html', context=context)


@login_required
def collect_book(request):
    id = request.GET.get('book-id', None)
    if not id:
        raise Http404
    else:
        book = get_object_or_404(Book, id=id)
        if request.user.collect_book(book):
            messages.success(request, "你成功收藏了 {title}".format(title=book.name))
        else:
            messages.info(request, '你已经收藏过 {title}，不能再次收藏'.format(title=book.name))

        redirect_url = reverse('Content:book', kwargs={'slug': book.slug})
        return redirect(redirect_url)


@login_required
def remove_collected_book(request):
    id = request.GET.get('book-id', None)
    if not id:
        raise Http404
    else:
        book = get_object_or_404(Book, id=id)
        if request.user.remove_collected_book(book):
            messages.success(request, "你从收藏夹中删除了图书 {title}".format(title=book.name))
        else:
            messages.info(request, "你还没有收藏过图书 {title}".format(title=book.name))

        redirect_url = reverse('Content:book', kwargs={'slug': book.slug})
        return redirect(redirect_url)


@login_required
def collection_books(request):
    books = request.user.collection.books.all()
    context = {
        'books': books,
    }
    return render(request, 'Content/collection_books.html', context=context)
