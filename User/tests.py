from django.test import TestCase

from .models import User


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User(username='test', password='testtest')
        self.user.save()

    def test_inherit_ship(self):
        from django.contrib.auth.models import AbstractUser
        self.assertTrue(isinstance(self.user, AbstractUser))

    def test_default_avatar(self):
        real_path = self.user.avatar.path
        default_path = self.user.avatar.field.default.replace('/', '\\')

        self.assertTrue(default_path in real_path)

    def test_right_token(self):
        user = User.objects.first()
        token = user.generate_token(True)
        info = user.load_token(token)

        self.assertTrue(info['info'])

    def test_error_token(self):
        user = User.objects.first()
        token = user.generate_token(True) + 'error'
        info = user.load_token(token)

        self.assertFalse(info)

    def test_expired_token(self):
        user = User.objects.first()
        token = user.generate_token(True)
        info = user.load_token(token, expiration=0)

        self.assertFalse(info)
