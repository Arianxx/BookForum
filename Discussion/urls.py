from django.urls import path

from .views import *

app_name = 'Discussion'
urlpatterns = [
    path('', DiscussView.as_view(), name='discussions'),
    path('hot-discussions', all_hot_dicussions, name='hot_discussions'),
    # path('detail/<str:slug>', )
]
