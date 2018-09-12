from django.urls import path, include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = 'Discussion'
urlpatterns = [
    path('', DiscussView.as_view(), name='discussions'),
    path('notification', login_required(NotificationView.as_view()), name='notifications'),
    path('hot-discussions', all_hot_dicussions, name='hot_discussions'),
    path('discussion/<pk>', DiscussionView.as_view(), name='discussion_detail'),
    path('<str:book_slug>/post-discussion', post_discussion, name='post_discussion'),
    path('<pk>/post-reply', post_reply, name='post_reply'),

    path('collect-discussion', collect_discussion, name='collect_discussion'),
    path('remove-collected-discussion', remove_collected_discussion, name='remove_collected_discussion'),
    path('collection-discussions', collection_discussions, name='collection_discussions'),

    path('search/', include('haystack.urls'), name='search')
]
