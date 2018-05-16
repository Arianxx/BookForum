from django.contrib import admin
from .models import Book, Publishing, Auther, Tag, Poll, Discuss, DiscussReply

# Register your models here.

# 自定义管理界面标题
admin.site.site_header = '后台管理'
admin.site.site_title = '后台管理'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # 可供排序的列名
    list_display = ('name', 'pub_date', 'auther', 'publishing', 'poll_count')

    # 可以按照出版时间筛选
    date_hierarchy = 'pub_date'

    # 供过滤的列
    list_filter = ('auther', 'tags', 'publishing',)

    # 添加额外的多对多关系编辑样式
    filter_horizontal = ('tags',)

    # 启用编辑的字段
    fields = ('name', 'pub_date', 'auther', 'publishing', 'tags',)

    # 可供搜索的列
    search_fields = ['name']

    def poll_count(self, obj):
        """
        一个粗略的计票统计字段。
        TODO:使用更好的计算方式
        :param obj: 模型对象自身
        :return: 赞同票与反对票的差值
        """
        return obj.poll.up - obj.poll.down

    poll_count.short_description = 'poll count'
    poll_count.admin_order_field = 'poll'


@admin.register(Auther)
class AutherAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'location', 'books_count')

    fields = ('name', 'age', 'location')

    def books_count(self, obj):
        return obj.books.count()

    books_count.short_description = "books count"


@admin.register(Publishing)
class PublishingAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'books_count')

    filter_horizontal = ('books',)

    def books_count(self, obj):
        return obj.books.count()

    books_count.short_description = 'books count'


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('book', 'up', 'down',)


@admin.register(Discuss)
class DiscussAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'book', 'replys_count')

    list_filter = ('pub_date', 'book',)

    date_hierarchy = 'pub_date'

    def replys_count(self, obj):
        return obj.replys.count()

    replys_count.short_description = 'replys count'


@admin.register(DiscussReply)
class DiscussReplyAdmin(admin.ModelAdmin):
    list_display = ('discuss', 'pub_date')

    list_filter = ('pub_date', 'discuss',)

    date_hierarchy = 'pub_date'
