from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path

from .views import register, profile, profile_edit, avatar_edit, password_change, email_change, email_change_confirm, \
    UserPersonalView, UserAllDiscussion, UserAllReplys

app_name = 'User'
urlpatterns = [
    path('login', LoginView.as_view(template_name='Auth/login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='Auth/logout.html'), name='logout'),
    path('password-change', password_change, name='password_change'),
    path('password-reset', PasswordResetView.as_view(
        template_name='Auth/password_reset.html',
        email_template_name='Auth/email/password_reset_email.html',
        subject_template_name='Auth/email/password_reset_subject.txt',
        success_url='User:password_reset_done',
        from_email=getattr(settings, 'EMAIL_FROM'),
    ), name='password_reset'),
    path('password-reset-done', PasswordResetDoneView.as_view(template_name='Auth/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(
            template_name='Auth/password_reset_confirm.html',
            success_url='User:password_reset_complete',
    ), name='password_reset_confirm'),
    path('password-reset-complete', PasswordResetCompleteView.as_view(template_name='Auth/password_reset_complete.html'),
         name='password_reset_complete'),
    path('register', register, name='register'),
    path('profile', profile, name='profile'),
    path('email-change', email_change, name='email_change'),
    path('email-change-confirm/<token>', email_change_confirm, name="email_change_confirm"),
    path('profile-edit', profile_edit, name='profile_edit'),
    path('avatar-edit', avatar_edit, name='avatar_edit'),
    path('user/<str:slug>', UserPersonalView.as_view(), name="user"),
    path('user/<str:slug>/discussions', UserAllDiscussion.as_view(), name='user_discussions'),
    path('user/<str:slug>/replys', UserAllReplys.as_view(), name='user_replys'),
]
