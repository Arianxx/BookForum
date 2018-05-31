from django.urls import path

from .views import *

app_name = 'Discussion'
urlpatterns = [
    path('', DiscussView.as_view(), name='discussions'),
    path('hot-discussions', all_hot_dicussions, name='hot_discussions'),
    path('discussion/<pk>', DiscussionView.as_view(), name='discussion_detail'),
    path('<str:book_slug>/post-discussion', post_discussion, name='post_discussion'),
    path('<pk>/post-reply', post_reply, name='post_reply'),
]
