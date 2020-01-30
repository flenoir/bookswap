from django.shortcuts import render, get_object_or_404
from .models import Book
from users.models import CustomUser
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
        # print('toto is :', toto)
        print('isbn is :', isbn)
        for i in toto:
            if i['volumeInfo']['industryIdentifiers'][0]['identifier'] == isbn:
                print("found match !")
                print("user is:", request.user.username)
                
                # save book

                try:
                    book_to_save = Book(
                        isbn=i['volumeInfo']['industryIdentifiers'][0]['identifier'],
                        title=i['volumeInfo']['title'],
                        author=i['volumeInfo']['authors'],
                        cover=i['volumeInfo']['imageLinks']['thumbnail'],
                        publisher = i['volumeInfo']['publisher'],
                        description = i['volumeInfo']['description'],
                        category = i['volumeInfo']['categories'],
                        page_count  = i['volumeInfo']['pageCount'],
                        state = "good condition",
                        availability = True,
                        published_date = i['volumeInfo']['publishedDate'][:10],

                    )
                    book_to_save.save()
                    current_user = request.user
                    book_to_associate = Book.objects.get(isbn=i['volumeInfo']['industryIdentifiers'][0]['identifier'])
                    current_user.user_books.add(book_to_associate)                    
                    print("book_list is:", request.user.user_books)
                    # maybe add a popup or flash notice message to say that book has been saved
                    print("saved")
                except Exception as e:
                    print("not saved :", e)
    

            else:
                print("not matched")
        return render(request, 'main.html', {'result': toto})
    else:
        print("save method had been called !")
    # print(data)

def remove_book(request, isbn):
    if request.method == 'POST':
        request.user.user_books.remove(isbn)
        books = CustomUser.objects.filter(user_books__isnull=False).filter(id=request.user.id)
        main_book_list = [i for i in books]
        sub_books = [j for j in main_book_list[0].user_books.all()]
        context = {"full_list": sub_books}
        return render(request, 'book_list.html', context)

   
def book_list(request):
    # select all uuid of current user book list    
    books = CustomUser.objects.filter(user_books__isnull=False).filter(id=request.user.id)
    main_book_list = [i for i in books]
    sub_books = [j for j in main_book_list[0].user_books.all()]
    print(sub_books)
    context = {"full_list": sub_books}
    return render(request, 'book_list.html', context)

 



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
            return render(request, "main.html", context)
        return render(request, "main.html", {"form": form})