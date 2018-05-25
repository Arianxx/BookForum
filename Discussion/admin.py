from django.contrib import admin

from .models import Discuss
from .models import DiscussReply


# Register your models here.

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
