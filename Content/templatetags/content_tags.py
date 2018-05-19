from django import template
from django.db.models.aggregates import Count
import random
from ..models import Book, Poll, Discuss, Tag

register = template.Library()


@register.simple_tag()
def get_tags(book_object):
    """
    获取一本书的所有标签。

    :param book_object: Book模型实例
    :return: Tag模型列表
    """
    return book_object.tags.all()


@register.simple_tag()
def get_all_tags():
    """
    获得所有的标签

    :return: Tag模型实例的列表
    """
    return Tag.objects.all()


@register.simple_tag()
def get_discussions_number(book_object):
    """
    获得本书讨论的数量。

    :param book_object: Book模型实例
    :return: Tag模型标签
    """
    return book_object.discussions.count()

@register.simple_tag()
def get_replys_number(discussion_object):
    return discussion_object.replys.count()

@register.simple_tag()
def get_discussion_replys(discussion, sort="-pub_date", num=1):
    num = int(num)
    replys = discussion.replys.order_by(sort)[:num]
    return replys

@register.simple_tag()
def get_books(sort='book.pub_date', num=5):
    """
    得到按照指定排序方式的指定数量的书籍

    :param sort: 一个指定排序方式的字符串。
    :param num: 想获得书籍数量
    :return: Book实例的列表
    """
    return Book.objects.order_by(sort).all()[:num]


@register.simple_tag()
def get_hot_books(num=5):
    """
    因为计票信息单独在一个表，上面那个无法查询，所以单独列出来.

    :param num: 想要得到的书籍的数量
    :return: Book模型实例的集合
    """
    polls = Poll.objects.order_by('-up').all()[:num]
    books = [poll.book for poll in polls]
    return books


@register.simple_tag()
def get_hot_discussions(num=5):
    """
    得到指定数量的热门讨论

    :param num: 想要得到的讨论数量
    :return: Discuss模型的实例列表
    """
    discussions = Discuss.objects.annotate(reply_num=Count('replys')).all()
    discussions = sorted(discussions, key=lambda x: x.reply_num)
    return discussions[:num]


@register.simple_tag()
def get_random_color():
    """
    获得一个随机的bootstrap颜色字符串标识

    :return: bootstrap颜色字符串
    """
    color_str = [
        'primary',
        'secondary',
        'success',
        'danger',
        'warning',
        'info',
        'dark',
    ]
    return random.choice(color_str)


@register.inclusion_tag('Content/tag/show_books.html')
def show_books(object_list):
    """
    加载指定书籍列表的模板。

    :param object_list: Book模型实例的列表
    :return: 返回一个字典作为模板的上下文
    """
    context = {
        'books_list': object_list,
    }
    return context

@register.inclusion_tag('Content/tag/show_discussions.html')
def show_discussions(discussions_list):
    """
    加载指定讨论列表的模板

    :param dicussions_list:
    :return: 返回一个字典作为模板的上下文
    """
    context = {
        'discussions_list': discussions_list,
    }
    return context

@register.inclusion_tag('Content/tag/paginator.html')
def paginate(paginator, page, other=None, limit=1):
    """
    分页器标签。传入指定的参数，返回分页模板

    :param paginator: 分页器对象
    :param page: 当前页对象
    :param other: 额外传入url的参数
    :param limit: 显示当前页左右页码的数量
    :return: 返回一个字典作为模板的上下文
    """
    all_pages = paginator.num_pages
    now_page = page.number

    #根据当前页数和limit生成页码范围，None是页码之间的省略
    if (all_pages <= limit * 2 + 1):
        page_range = paginator.page_range
    else:
        if (now_page - limit <= 2):
            page_range = list(range(1, now_page+2)) + [None] \
                         + list(range(all_pages-limit, all_pages+1))
        elif (all_pages - now_page <= 2):
            page_range = list(range(1, limit+1)) + [None] \
                         + list(range(now_page-1, all_pages+1))
        else:
            page_range = list(range(1, limit+1)) + [None] \
                         + list(range(now_page-limit, now_page+limit+1)) + [None] \
                         + list(range(all_pages-limit+1, all_pages+1))

    context = {
        'paginator': paginator,
        'page': page,
        'page_range': page_range,
        'other': other,
    }
    return context
