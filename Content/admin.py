from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import Book, Publishing, Auther, Tag, Carousel

# Register your models here.

# 自定义管理界面标题
admin.site.site_header = '后台管理'
admin.site.site_title = '后台管理'


@admin.register(Book)
class BookAdmin(GuardedModelAdmin, admin.ModelAdmin):
    # 列名
    list_display = ('name', 'pub_date', 'auther', 'publishing', 'viewing')

    # 可以按照出版时间筛选
    date_hierarchy = 'pub_date'

    # 供过滤的列
    list_filter = ('auther', 'tags', 'publishing',)

    # 添加额外的多对多关系编辑样式
    filter_horizontal = ('tags',)

    # 启用编辑的字段
    fields = ('name', 'pub_date', 'auther', 'publishing', 'cover', 'intro', 'tags')

    # 启用搜索的外键编辑字段
    raw_id_fields = ('auther', 'publishing',)

    # 可供搜索的列
    search_fields = ['name']


@admin.register(Auther)
class AutherAdmin(GuardedModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'books_count')

    fields = ('name', 'about')

    def books_count(self, obj):
        return obj.books.count()

    books_count.short_description = "books count"


@admin.register(Publishing)
class PublishingAdmin(GuardedModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'establish_date',)

    fields = ('name', 'establish_date', 'about',)

    list_filter = ('establish_date',)

    date_hierarchy = 'establish_date'


@admin.register(Tag)
class TagAdmin(GuardedModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'books_count')

    filter_horizontal = ('books',)

    def books_count(self, obj):
        return obj.books.count()

    books_count.short_description = 'books count'


@admin.register(Carousel)
class CarouselAdmin(GuardedModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'img', 'title')
