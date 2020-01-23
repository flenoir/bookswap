from django.shortcuts import render
from .models import Book
from django.urls import reverse_lazy
from .form import BookForm, SearchForm

import json
import requests


def isbn_text_search(isbn):
    # Voir si pertinent de resoumettre la requete sur le titre pour avoir la cover
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q='+ isbn)
    # print(r.text)
    parsed = json.loads(r.text)
    # print(parsed['items'][0]['volumeInfo']['title'])  
    return parsed['items']

def input_cleaner(search_data):
    try:
        if type(int(search_data)):
            res = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:'+ str(search_data))
            parsed_res = json.loads(res.text)
            return parsed_res['items'][0]['volumeInfo']['title']
    except ValueError as error:
        print(error)
        return search_data

def save_book(request, isbn):
    if request.method == "POST":
        toto = request.session.get('temp_json')
        print('toto is :', toto)
        print('isbn is :', isbn)
        for i in toto:
            if i['volumeInfo']['industryIdentifiers'][0]['identifier'] == isbn:
                print("found match !")
                # save book

                try:
                    book_to_save = Book(
                        isbn=i['volumeInfo']['industryIdentifiers'][0]['identifier'],
                        title=i['volumeInfo']['title'],
                        author=i['volumeInfo']['authors'],
                    )
                    book_to_save.save()
                    print("saved")
                except Exception as e:
                    print("not saved :", e)
    

            else:
                print("not matched")
        return render(request, 'main.html', {'result': toto})

    # print(data)
   



def main(request):
    if request.method == "POST":
        print('post')
        # toto = request.session.get('temp_json')
        # print('toto is :', toto)
        return render(request, 'main.html')
    else:
        print('get')
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data["post"].casefold()
            # check if input is isbn number or title
            checked_input = input_cleaner(str(data))
            # search on title
            result = isbn_text_search(str(checked_input))
            request.session['temp_json'] = result
            context = {"form": form, "result": result}
            # book_save(result[0])
            return render(request, "main.html", context)
        return render(request, "main.html", {"form": form})