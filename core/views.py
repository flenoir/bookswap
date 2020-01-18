from django.shortcuts import render
# from django.views.generic import TemplateView, FormView
from .models import Book
from django.urls import reverse_lazy
from .form import BookForm, SearchForm

# from isbnlib import meta
# from isbnlib.registry import bibformatters
from isbnlib import canonical, meta, cover, desc


# Create your views here.

def isbn_search(isbn):
    # SERVICE = 'openl'
    # bibtex = bibformatters['bibtex']
    # print(bibtex(meta(isbn, SERVICE)))
    isbn = canonical("9782744145261")
    # data = meta(isbn)
    # print(data)
    Service = 'openl'
    # Service = 'goob'
    book = meta(isbn, Service)
    print(book)
    print(desc(isbn))
    bookCover = cover(isbn)
    print(bookCover)


def main(request):
    if request.method == "POST":
        print('post')
        return render(request, 'main.html')
    else:
        print('get')
        form = SearchForm(request.GET)
        # print(form)
        if form.is_valid():
            data = form.cleaned_data["post"].casefold()
            # print(data)
            result = data
            isbn_search(str(data))
            context = {"form": form, "result": result}
            return render(request, "main.html", context)
        return render(request, "main.html", {"form": form})