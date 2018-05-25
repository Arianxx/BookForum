from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from Content.common_tools import crop_img, delete_img


# Create your models here.

class User(AbstractUser):
    link = models.URLField("个人网站", blank=True)
    avatar = models.ImageField('用户头像', upload_to='avatar/%Y/%m/%d', default='avatar/default.jpg')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ('-date_joined',)

    def __str__(self):
        return 'User(username=%s)' % self.username

    def save(self, *args, **kwargs):
        default_avatar_path = self.avatar.field.default.replace('/', '\\')
        if not default_avatar_path in self.avatar.path:
            # 只剪裁用户上传的头像，不剪裁默认头像
            # TODO 头像长宽设置
            AVATAR_WIDTH = getattr(settings, 'AVATAR_WIDTH', 200)
            AVATAR_HEIGHT = getattr(settings, 'AVATAR_HEIGHT', 200)
            crop_img(self.avatar, AVATAR_WIDTH, AVATAR_HEIGHT)

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        delete_img(self.avatar)

        return super().delete(*args, **kwargs)
