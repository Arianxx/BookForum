from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView

from Content.common_tools import send_mail_thread
from .forms import RegisterForm, ProfileForm, AvatarForm, PasswordChangeForm, EmailChangeForm
from .models import User


class UserPersonalView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'Auth/user_personal.html'
    # TODO：增加用户个性页面


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                email=data['email'],
            )
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.is_confirmed = False

            user.save()
            messages.success(request, '你成功注册了一个用户')

            redirect_url = reverse('Content:index')
            return redirect(redirect_url)
    else:
        form = RegisterForm()

    return render(request, 'Auth/register.html', context={
        'form': form,
    })


@login_required
def profile(request):
    return render(request, 'Auth/profile.html')


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        form.user = request.user
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            user.username = data['username']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.birth = data['birth']
            user.link = data['link']
            user.about = data['about']

            user.save(update_fields=[
                'username',
                'first_name',
                'last_name',
                'birth',
                'link',
                'about'
            ])
            messages.success(request, '成功更新个人资料')

            redirect_url = reverse('User:profile')
            return redirect(redirect_url)
    else:
        form = ProfileForm()
        user = request.user
        form.data['username'] = user.username
        form.data['email'] = user.email
        form.data['first_name'] = user.first_name
        form.data['last_name'] = user.last_name
        form.data['birth'] = user.birth
        form.data['link'] = user.link
        form.data['about'] = user.about

    form['email'].errors.append('此字段不可在此编辑')
    return render(request, 'Auth/profile_edit.html', context={
        'form': form,
    })


@login_required
def avatar_edit(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.avatar = form.cleaned_data['avatar']
            request.user.save()

            messages.success(request, '成功修改头像')

            redirect_url = reverse('User:avatar_edit')
            return redirect(redirect_url)

    else:
        form = AvatarForm()
        form.data['avatar'] = request.user.avatar

    return render(request, 'Auth/avatar_edit.html', context={
        'form': form,
    })


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        form.user = request.user
        if form.is_valid():
            password = form.cleaned_data['new_password1']
            request.user.set_password(password)
            request.user.save()
            logout(request)

            messages.success(request, '成功修改密码，请重新登陆')

            redirect_url = reverse('User:login')
            return redirect(redirect_url)
    else:
        form = PasswordChangeForm()

    return render(request, 'Auth/password_change.html', context={
        'form': form,
    })


@login_required
def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        form.user = request.user
        if form.is_valid():
            email = form.cleaned_data['new_email']
            token = request.user.generate_token({'new_email': email})

            scheme = request.scheme
            host = request.get_host()
            domain = scheme + '://' + host

            send_mail_thread('更换邮箱', 'Auth/email/change_email.txt', [email, ], token=token, form=form, domain=domain)
            return render(request, 'Auth/change_email_done.html')
    else:
        form = EmailChangeForm()

    return render(request, 'Auth/change_email.html', context={
        'form': form,
    })


def email_change_confirm(request, token=''):
    key = User.load_token(token, 60 * 30)
    if not key:
        validlink = False
    else:
        id = key['id']
        email = key['info']['new_email']
        user = User.objects.get(id=id)
        user.email = email
        user.save(update_fields=['email', ])

        validlink = True

    return render(request, 'Auth/change_email_confirm.html', context={
        'validlink': validlink,
    })
