from django.shortcuts import render
# from django.views.generic import TemplateView, FormView
from .models import Book
from django.urls import reverse_lazy
from .form import BookForm, SearchForm

# from isbnlib import meta
# from isbnlib.registry import bibformatters
from isbnlib import canonical, meta, cover, desc
from isbntools.app import *

import json
from urllib.request import urlopen

import requests


def isbn_search(isbn):
    # Voir si pertinent de resoumettre la requette sur le titrre pour avoir la cover
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:'+ isbn)
    print(r.text)
    parsed = json.loads(r.text)
    # print(parsed['items'][0]['volumeInfo']['title'])
    return parsed['items'][0]['volumeInfo']

def main(request):
    if request.method == "POST":
        print('post')
        return render(request, 'main.html')
    else:
        print('get')
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data["post"].casefold()
            result = isbn_search(str(data))
            context = {"form": form, "result": result}
            return render(request, "main.html", context)
        return render(request, "main.html", {"form": form})