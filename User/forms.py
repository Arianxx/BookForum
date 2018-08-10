import datetime
import re

from django import forms
from django.contrib.auth.hashers import check_password

from .models import User


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=32, required=True)
    password = forms.CharField(label="密码", max_length=32, required=True)
    first_name = forms.CharField(label="名", max_length=32, required=False)
    last_name = forms.CharField(label="姓", max_length=32, required=False)
    email = forms.EmailField(label="邮箱", required=True)

    def clean_username(self):
        username = self.cleaned_data['username']

        re_parttern = r'^[a-zA-Z]{1}[0-9a-zA-Z_]*$'
        if not re.match(re_parttern, username):
            raise forms.ValidationError('用户名只能包含字母、数字和下划线，且必需以字母开头')

        user = User.objects.filter(username=username).all()
        if user:
            raise forms.ValidationError('此用户名已经被占用')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        re_parttern = r'^[0-9a-zA-Z]+@[0-9a-zA-Z-]+.[a-zA-Z]+$'
        if not re.match(re_parttern, email):
            raise forms.ValidationError('请输入正确的邮箱格式')

        user = User.objects.filter(email=email).all()
        if user:
            raise forms.ValidationError('此邮箱已经存在')

        return email

    def clean_password(self):
        password = self.cleaned_data['password']

        if not 8 <= len(password) <= 16:
            raise forms.ValidationError('密码长度必须在8~16之间')

        re_parttern = r'^[0-9a-zA-Z+-]+$'
        if not re.match(re_parttern, password):
            raise forms.ValidationError('密码只能包含数字、字母和加减号')

        return password

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if not len(first_name) <= 32:
            raise forms.ValidationError('姓名长度需小于32位')

        re_parttern = r'^[a-zA-Z]+$'
        if not re.match(re_parttern, first_name):
            raise forms.ValidationError('姓名只能包含大小写字母')

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if not len(last_name) <= 32:
            raise forms.ValidationError('姓名长度需小于32位')

        re_parttern = r'^[a-zA-Z]+$'
        if not re.match(re_parttern, last_name):
            raise forms.ValidationError("姓名只能包含大小写字母")

        return last_name


class ProfileForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32, required=True)
    email = forms.EmailField(label='邮箱', required=False)
    first_name = forms.CharField(label='名', max_length=32, required=False)
    last_name = forms.CharField(label='姓', max_length=32, required=False)
    birth = forms.DateField(label='生日', required=False)
    link = forms.URLField(label='个人网站', required=False)
    about = forms.CharField(label='关于我', max_length=512, required=False)

    clean_first_name = RegisterForm.clean_first_name
    clean_last_name = RegisterForm.clean_last_name

    def clean_username(self):
        username = self.cleaned_data['username']

        re_parttern = r'^[a-zA-Z]{1}[0-9a-zA-Z_]*$'
        if not re.match(re_parttern, username):
            raise forms.ValidationError('用户名只能包含字母、数字和下划线，且必需以字母开头')

        user = User.objects.filter(username=username).all()
        if len(user) != 1 or user[0].username != self.user.username:
            raise forms.ValidationError('此用户名已被占用')

        return username

    def clean_birth(self):
        birth = self.cleaned_data['birth']
        if not birth:
            return birth

        now = datetime.datetime.now()

        if birth.year > now.year or birth.year < now.year - 100:
            raise forms.ValidationError('生日年份必需介于 %d~%d 之间' % (now.year - 100, now.year))


class AvatarForm(forms.Form):
    avatar = forms.ImageField(label="头像", allow_empty_file=True)


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label="原始密码", min_length=8, max_length=32)
    new_password1 = forms.CharField(label="新密码", min_length=8, max_length=32)
    new_password2 = forms.CharField(label="重复密码", min_length=8, max_length=32)

    def clean_new_password2(self):
        password2 = self.cleaned_data.get('new_password1')
        password1 = self.cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('两个新密码必需相等')

        re_parttern = r'^[0-9a-zA-Z+-]+$'
        if not re.match(re_parttern, password1):
            raise forms.ValidationError('密码只能包含数字、字母和加减号')

        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if not check_password(old_password, self.user.password):
            raise forms.ValidationError('密码错误')
        else:
            return old_password


class EmailChangeForm(forms.Form):
    password = forms.CharField(label='密码', min_length=8, max_length=16, required=True)
    new_email = forms.EmailField(label='新邮箱', required=True)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not check_password(password, self.user.password):
            raise forms.ValidationError('密码错误')
        else:
            return password

    def clean_new_email(self):
        email = self.cleaned_data['new_email']

        re_parttern = r'^[0-9a-zA-Z]+@[0-9a-zA-Z-]+.[a-zA-Z]+$'
        if not re.match(re_parttern, email):
            raise forms.ValidationError('请输入正确的邮箱格式')

        user = User.objects.filter(email=email).all()
        if user:
            raise forms.ValidationError('此邮箱已经存在')

        return email
