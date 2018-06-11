from django import forms

from .models import Book, Auther, Publishing, Tag


class AddNodeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'intro', 'cover', 'publishing', 'auther', 'tags']


class AddAutherForm(forms.ModelForm):
    class Meta:
        model = Auther
        fields = ['name', 'about']


class AddPublishingForm(forms.ModelForm):
    class Meta:
        model = Publishing
        fields = ['name', 'establish_date', 'about']


class AddTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
