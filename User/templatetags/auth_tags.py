from django import template

register = template.Library()


@register.inclusion_tag('tag/common_field.html')
def field(field):
    """
    返回一个常用的渲染表单字段的html代码

    :param field: 将要渲染的表单字段对象
    :return: 用在模板里的上下文
    """
    context = {
        'field': field,
    }
    return context
