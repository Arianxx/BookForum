from django.urls import path
from .views import *

app_name = 'books'
urlpatterns = [
    path('hello', hello, name='hello'),
]