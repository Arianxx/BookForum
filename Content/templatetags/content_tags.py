import random

from django import template

from ..models import Book, Tag, Carousel

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
    :param num: 想要得到的书籍的数量
    :return: Book模型实例的集合
    """
    books = Book.objects.order_by('-viewing').all()[:num]
    return books


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


@register.inclusion_tag('tag/show_books.html')
def show_books(object_list):
    """
    加载指定书籍列表的模板。

    :param object_list: Book模型实例的列表
    :return: 返回一个字典作为模板的上下文
    """
    if len(object_list) > 0:
        try:
            getattr(object_list[0], 'object')
        except AttributeError:
            pass
        else:
            object_list = map(lambda ele: ele.object, object_list)

    context = {
        'books_list': object_list,
    }
    return context


@register.inclusion_tag('tag/show_carousel.html')
def show_carousel():
    """
    加载展示头图的模板。头图储存于Carousel模型中

    :return: Carousel对象的集合
    """
    context = {
        "carousels": Carousel.objects.all(),
    }
    return context


@register.inclusion_tag('tag/paginator.html')
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

    # 根据当前页数和limit生成页码范围，None是页码之间的省略
    if (all_pages <= limit * 4 + 1):
        page_range = paginator.page_range
    else:
        if (now_page - limit <= 2):
            page_range = list(range(1, now_page + 2)) + [None] \
                         + list(range(all_pages - limit, all_pages + 1))
        elif (all_pages - now_page <= 2):
            page_range = list(range(1, limit + 1)) + [None] \
                         + list(range(now_page - 1, all_pages + 1))
        else:
            page_range = list(range(1, limit + 1)) + [None] \
                         + list(range(now_page - limit, now_page + limit + 1)) + [None] \
                         + list(range(all_pages - limit + 1, all_pages + 1))

    context = {
        'paginator': paginator,
        'page': page,
        'page_range': page_range,
        'other': other,
    }
    return context
