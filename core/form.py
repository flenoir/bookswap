from django import forms

from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('isbn', 'title', 'author')

class SearchForm(forms.Form):
    post = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'ISBN, Title or author', 'size': '100'}))