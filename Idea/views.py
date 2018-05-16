from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Book

# Create your views here.

class IndexView(generic.ListView):
    models = Book
    context_object_name = 'Books'
    template_name = 'Idea/index.html'
    allow_empty = False
