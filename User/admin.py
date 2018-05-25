from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as original_UserAdmin

from .models import User


# Register your models here.

@admin.register(User)
class UserAdmin(original_UserAdmin):
    # 继承自原本的用户管理类，但添加了自定义的字段
    fieldsets = tuple(list(original_UserAdmin.fieldsets) +
                      [(('个性化信息', {'fields': ('link', 'avatar',)}))]
                      )
