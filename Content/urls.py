from django.urls import path
from .views import *

app_name = 'Content'
urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('discussions/', DiscussView.as_view(), name='discussions'),
]