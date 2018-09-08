import re
from copy import copy

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from Content.models import Book
from User.models import User
from .forms import DiscussionForm, ReplyForm
from .models import Discuss, DiscussReply, Notification


# Create your views here.

class DiscussView(generic.ListView):
    model = Discuss
    context_object_name = 'Discussions'
    template_name = 'Discussion/discussions.html'
    paginate_by = getattr(settings, 'PER_PAGE_SHOW', 20)
    paginate_orphans = getattr(settings, 'ORPHANS_PAGE_SHOW', 5)

    def get_ordering(self):
        sort = self.kwargs.get('sort', '-pub_date')
        return (str(sort), '-pub_date', '-id')


class DiscussionView(generic.DetailView):
    model = Discuss
    context_object_name = 'discussion'
    template_name = 'Discussion/discussion_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object.book
        context['book'] = book

        # 从session里获取暂存的表单信息，获取后就将其删除
        form = self.request.session.get('ReplyForm')
        context['form'] = form
        self.request.session['ReplyForm'] = None
        return context


class NotificationView(generic.ListView):
    model = User
    context_object_name = 'Notifications'
    template_name = 'Discussion/notification.html'
    paginate_by = getattr(settings, 'PER_PAGE_SHOW', 10)
    paginate_orphans = getattr(settings, 'ORPHANS_PAGE_SHOW', 5)

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.get(id=self.request.user.id).receive_notifies.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.unread = []
        context['notifications'] = list(filter(lambda x: not x.is_read, context['Notifications']))
        self.request.unread.extend(context['notifications'])
        context['notifications'].extend(list(filter(lambda x: x.is_read, context['Notifications'])))
        return context

    def get(self, *args, **kwargs):
        response = super().get(self.request, *args, **kwargs)
        self.mark_notify_to_read(self.request.unread)
        return response

    def mark_notify_to_read(self, notifies):
        # 为了不影响渲染，使用copy
        list(map(lambda notify: copy(notify).mark_to_read(), notifies))


def all_hot_dicussions(request):
    discussions = Discuss.objects.annotate(reply_num=Count('replys')).all()[:10]
    discussions = sorted(discussions, key=lambda x: x.reply_num, reverse=True)

    context = {
        'discussions': discussions,
    }
    return render(request, 'Discussion/hot_discussions.html', context=context)


@login_required
def post_discussion(request, book_slug=''):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            book = get_object_or_404(Book, slug=book_slug)
            user = request.user
            discuss = Discuss(
                title=data['title'],
                body=data.get('body'),
                book=book,
                user=user,
            )
            discuss.save()
            discuss.mentions.set(get_mention_users(data))
            discuss.save()

            messages.success(request, '你成功发布了一个帖子')

            redirect_url = reverse('Discussion:discussion_detail', kwargs={'pk': discuss.pk})
            return redirect(redirect_url)
        else:
            data = form.cleaned_data
    else:
        form = None
        data = {}

    # 在提交Post的视图和展示讨论的书籍之间传递表单的信息，以在表单提交失败的情况下保留表单
    request.session['DiscussionForm'] = {
        'title': data.get('title'),
        'body': data.get('body'),
    }
    if form:
        # 同时储存错误信息
        request.session['DiscussionForm']['errors'] = ''.join(
            [('帖子标题：' + ''.join(form['title'].errors)) if form['title'].errors else '',
             ('帖子正文：' + ''.join(form['body'].errors)) if form['body'].errors else '',
             ]
        )
    # 明确改变了session，以使其实际生效
    request.session.modified = True

    redirect_url = reverse('Content:book', args={book_slug})
    return redirect(redirect_url)


@login_required
def post_reply(request, pk=''):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            discussion = get_object_or_404(Discuss, id=int(pk))
            data = form.cleaned_data

            reply = DiscussReply(
                body=data['body'],
                discuss=discussion,
                user=request.user,
            )
            reply.save()
            reply.mentions.set(get_mention_users(data))
            reply.save()

            messages.success(request, '你成功添加了一条回复')

            redirect_url = reverse('Discussion:discussion_detail', kwargs={'pk': discussion.pk})
            # 跳转后的链接指向自己回复的那一层
            redirect_url += '#' + str(reply.id)
            return redirect(redirect_url)
        else:
            data = form.cleaned_data
    else:
        form = None
        data = {}

    # 跨视图保存表单的数据
    request.session['ReplyForm'] = {
        'body': data.get('body'),
    }
    if form:
        request.session['ReplyForm']['errors'] = ''.join(
            ['回复正文' + ''.join(form['body'].errors) if form['body'].errors else '',
             ]
        )
    request.session.modified = True

    redirect_url = reverse('Discussion:discussion_detail', args=[pk])
    return redirect(redirect_url)


@login_required
def collect_discussion(request):
    id = request.GET.get('discussion-id', None)
    if not id:
        raise Http404
    else:
        discussion = get_object_or_404(Discuss, id=id)
        if request.user.collect_discussion(discussion):
            messages.success(request, "你成功收藏了这个话题")
        else:
            messages.info(request, "你已经收藏过这个话题")

        redirect_url = reverse('Discussion:discussion_detail', kwargs={'pk': discussion.pk})
        return redirect(redirect_url)


@login_required
def remove_collected_discussion(request):
    id = request.GET.get('discussion-id', None)
    if not id:
        raise Http404
    else:
        discussion = get_object_or_404(Discuss, id=id)
        if request.user.remove_collected_discussion(discussion):
            messages.success(request, "你从收藏夹中删除了这个话题")
        else:
            messages.info(request, "你无法删除没有收藏的话题")

        redirect_url = reverse('Discussion:discussion_detail', kwargs={"pk": discussion.pk})
        return redirect(redirect_url)


@login_required
def collection_discussions(request):
    discussions = request.user.collection.discussions.all()
    context = {
        'discussions': discussions,
    }
    return render(request, 'Discussion/collection_discussions.html', context=context)


def get_mention_users(data):
    mentions = map(lambda x: x.split('@')[1], re.findall(r'@\S*', data['body'], re.M))
    mention_users = map(lambda username: User.objects.filter(username=username).all(), mentions)
    return list(map(lambda x: x[0], filter(lambda x: len(x), mention_users)))