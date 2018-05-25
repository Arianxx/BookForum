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
]
