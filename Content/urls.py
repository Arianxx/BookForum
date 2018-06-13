from django.urls import path

from .views import *

app_name = 'Content'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('hot-book', all_hot_books, name='hot_books'),
    path('tag/<str:slug>', TagView.as_view(), name='tag'),
    path('auther/<str:slug>', AutherView.as_view(), name='auther'),
    path('publishing/<str:slug>', PublishingView.as_view(), name='publishing'),
    path('book/<str:slug>', BookView.as_view(), name='book'),

    path('add_node', add_node, name='add_node'),
    path('add_auther', add_auther, name='add_auther'),
    path('add_publishing', add_publishing, name='add_publishing'),
    path('add_tag', add_tag, name='add_tag'),

    path('collect-book/', collect_book, name='collect_book'),
    path('remove-collected-book/', remove_collected_book, name='remove_collected_book'),
    path('collection-books', collection_books, name='collection_books'),
]
