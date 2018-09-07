import re

from django import template
from django.db.models.aggregates import Count
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.shortcuts import reverse
from django.urls.exceptions import NoReverseMatch

from ..models import Discuss

register = template.Library()


@register.simple_tag()
def get_discussions_number(book_object):
    """
    获得本书讨论的数量。

    :param book_object: Book模型实例
    :return: 本书讨论数量
    """
    return book_object.discussions.count()


@register.simple_tag()
def get_discussions(book_object):
    """
    获得本书所有的讨论

    :param book_object: Book模型实例
    :return: 本书所有讨论的列表
    """
    return book_object.discussions.order_by('-pub_date').all()


@register.simple_tag()
def get_replys_number(discussion_object):
    return discussion_object.replys.count()


@register.simple_tag()
def get_discussion_replys(discussion, sort="-pub_date", num=1):
    num = int(num)
    if not num:
        replys = discussion.replys.order_by(sort).all()
    else:
        replys = discussion.replys.order_by(sort)[:num]

    return replys


@register.simple_tag()
def get_hot_discussions(num=5):
    """
    得到指定数量的热门讨论

    :param num: 想要得到的讨论数量
    :return: Discuss模型的实例列表
    """
    discussions = Discuss.objects.annotate(reply_num=Count('replys')).all()
    discussions = sorted(discussions, key=lambda x: x.reply_num, reverse=True)
    return discussions[:num]


def sub_match_reply(match):
    username = match.group()[1:]
    try:
        url = reverse("User:user", kwargs={"slug": username})
    except NoReverseMatch:
        url = username
    return '<a href="' + url + '">@' + username + '</a>'


@register.simple_tag()
def render_reply(reply):
    # 替换@的用户名为链接
    reply = escape(reply)
    return mark_safe(re.sub(r'@\S*', sub_match_reply, reply))


@register.simple_tag()
def unread_notifies_num(user):
    """
    得到user未读的通知数目
    :param user: User实例
    """
    return len(user.receive_notifies.filter(is_read=False).all())


@register.inclusion_tag('tag/show_discussions.html')
def show_discussions(discussions_list):
    """
    加载指定讨论列表的模板

    :param dicussions_list: 将要展现的讨论列表
    :return: 返回一个字典作为模板的上下文
    """
    context = {
        'discussions_list': discussions_list,
    }
    return context


@register.inclusion_tag('tag/show_book_detail.html')
def show_book_detail(book_object):
    """
    作为一个左边栏，展示书籍的详细信息

    :param book_object: Book模型的实例
    :return: 返回一个字典作为模板的上下文
    """
    context = {
        "book": book_object,
    }
    return context


@register.inclusion_tag('tag/show_discussion_detail.html')
def show_discussion_detail(reqeust, discussion_object):
    """
    加载指定讨论的详细信息模板

    :param discussion_object: 讨论(Discuss)模型的实例
    :return: 一个用于模板的上下文
    """
    context = {
        'discussion': discussion_object,
        "request": reqeust,
    }
    return context
