import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from uuslug import slugify

from Content.common_tools import crop_img, delete_img


# Create your models here.

class User(AbstractUser):
    birth = models.DateField('生日', null=True, blank=True)
    about = models.TextField('关于我', max_length=512, default='', blank=True)
    slug = models.SlugField('Slug', unique=True)

    link = models.URLField("个人网站", blank=True)
    avatar = models.ImageField('用户头像', upload_to='avatar/%Y/%m/%d', default='avatar/default.jpg')

    is_confirmed = models.BooleanField("验证邮箱", default=False)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ('-date_joined',)

    def __str__(self):
        return 'User(username=%s)' % self.username

    def save(self, *args, **kwargs):
        default_avatar_path = self.avatar.field.default.replace('/', '\\')
        origin_user = User.objects.get(id=self.id)
        if not default_avatar_path in origin_user.avatar.path:
            if origin_user.avatar.path != self.avatar.path:
                # 修改头像，删除原来头像
                try:
                    os.remove(origin_user.avatar.path)
                except FileNotFoundError:
                    pass

        self.slug = slugify(self.username)
        ret = super().save(*args, **kwargs)

        if not default_avatar_path in self.avatar.path:
            # 只剪裁用户上传的头像，不剪裁默认头像
            AVATAR_WIDTH = getattr(settings, 'AVATAR_WIDTH', 800)
            AVATAR_HEIGHT = getattr(settings, 'AVATAR_HEIGHT', 800)
            crop_img(self.avatar, AVATAR_WIDTH, AVATAR_HEIGHT)


        return ret

    def delete(self, *args, **kwargs):
        default_path = self.avatar.field.default.replace('/', '\\')
        if not default_path in self.avatar.path:
            delete_img(self.avatar)

        return super().delete(*args, **kwargs)

    def generate_token(self, info):
        serializer = URLSafeTimedSerializer(getattr(settings, 'SECRET_KEY'))
        key_info = {'id': self.id, 'info': info, }
        token = serializer.dumps(key_info)
        return token

    @staticmethod
    def load_token(token, expiration):
        serializer = URLSafeTimedSerializer(getattr(settings, 'SECRET_KEY'))
        try:
            key_info = serializer.loads(token, max_age=expiration)
            return key_info
        except SignatureExpired:
            return False
        except BadTimeSignature:
            return False
