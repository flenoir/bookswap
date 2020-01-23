from django.shortcuts import render
from .models import Book
from django.urls import reverse_lazy
from .form import BookForm, SearchForm

import json
import requests

class Search():
    temp_json = {}

    def input_cleaner(self, search_data):
        try:
            if type(int(search_data)):
                res = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:'+ str(search_data))
                parsed_res = json.loads(res.text)
                return parsed_res['items'][0]['volumeInfo']['title']
        except ValueError as error:
            print(error)
            return search_data

    def isbn_text_search(self, isbn):
        # Voir si pertinent de resoumettre la requette sur le titrre pour avoir la cover
        r = requests.get('https://www.googleapis.com/books/v1/volumes?q='+ isbn)
        # print(r.text)
        parsed = json.loads(r.text)
        temp_json = parsed
        print(temp_json)
        return parsed['items']



# def book_save(data):
#     try:
#         book_to_save = Book(
#             isbn=data.volumeInfo.isbn
#             title=data.volumeInfo.title
#             author=data.volumeInfo.author
#         )



def main(request):
    if request.method == "POST":
        print('post')
        return render(request, 'main.html')
    else:
        print('get')
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data["post"].casefold()

            current_search = Search()
            clean_res = current_search.input_cleaner(str(data))
            result = current_search.isbn_text_search(clean_res)

            # # check if input is isbn number or title
            # checked_input = input_cleaner(str(data))
            # # search on title
            # result = isbn_text_search(str(checked_input))
            # print("Yo", result)


            context = {"form": form, "result": result}
            return render(request, "main.html", context)
        return render(request, "main.html", {"form": form})