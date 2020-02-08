from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from users.models import CustomUser
from django.urls import reverse_lazy
from .form import BookForm, SearchForm, InviteForm
from invitations.utils import get_invitation_model

import json
import requests


def isbn_text_search(isbn):
    ''' 
    make a search request based on title or authors 
    '''
    # Voir si pertinent de resoumettre la requete sur le titre pour avoir la cover
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q='+ isbn)    
    parsed = json.loads(r.text)
    return parsed['items']

def input_cleaner(search_data):
    ''' 
    make a search request based on isbn number
    '''
    try:
        if type(int(search_data)):
            res = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:'+ str(search_data))
            parsed_res = json.loads(res.text)
            return parsed_res['items'][0]['volumeInfo']['title']
    except ValueError as error:
        print(error)
        return search_data

def save_book(request, isbn):
    ''' 
    save book on book table
    '''
    if request.method == "POST":
        data = request.session.get('temp_json')
        
        # print('isbn is :', isbn)
        for i in data:
            if i['volumeInfo']['industryIdentifiers'][0]['identifier'] == isbn:
                print("found match !")
                print("user is:", request.user.username)
                
                # save book

                try:
                    book, not_yet_created = Book.objects.get_or_create(isbn=isbn)
                    print(book)
                    print("created or not", not_yet_created)

                    if not_yet_created:
                        print('pas encore en base de donnée')
                        book.isbn=i['volumeInfo']['industryIdentifiers'][0]['identifier']
                        book.title=i['volumeInfo']['title']
                        book.author=i['volumeInfo']['authors']
                        book.cover=i['volumeInfo']['imageLinks']['thumbnail']
                        book.publisher = i['volumeInfo']['publisher']
                        book.description = i['volumeInfo']['description']
                        book.category = i['volumeInfo']['categories']
                        book.page_count  = i['volumeInfo']['pageCount']
                        book.state = "good condition"
                        book.availability = True
                        book.published_date = i['volumeInfo']['publishedDate'][:10]
                        book.save()
                        print("je l'associe à l'utilisateur courant")
                        current_user = request.user
                        book_to_associate = Book.objects.get(isbn=i['volumeInfo']['industryIdentifiers'][0]['identifier'])
                        current_user.user_books.add(book_to_associate) 
                    else:
                        print("le livre {} existe deja".format(book))
                        print("il existe déjà, mais j'essaye de l'associer à l'utilisateur courant")
                        current_user = request.user
                        book_to_associate, not_yet_associated = Book.objects.get_or_create(isbn=i['volumeInfo']['industryIdentifiers'][0]['identifier'])
                        if not_yet_associated:
                            current_user.user_books.add(book_to_associate)
                        else:
                            print("the user already has this book in his book list !") 
                        
                    print("saved")
                except Exception as e:
                    print("not saved :", e)
    

            else:
                print("not matched")
        return render(request, 'main.html', {'result': data})
    else:
        print("save method had been called !")
    

def book_search(request):
    ''' 
    select all uuid of current user book list
    '''
    books = CustomUser.objects.filter(user_books__isnull=False).filter(id=request.user.id)
    main_book_list = [i for i in books]
    sub_books = [j for j in main_book_list[0].user_books.all()]
    print(sub_books)
    context = {"full_list": sub_books}
    return context

def remove_book(request, isbn):
    ''' 
    remove book from user's list
    '''
    if request.method == 'POST':
        request.user.user_books.remove(isbn)
        context = book_search(request)       
        return render(request, 'book_list.html', context)

   
def book_list(request): 
    ''' 
    list all books saved by an user
    '''   
    context = book_search(request)    
    return render(request, 'book_list.html', context)


def book_detail(request, isbn):
    ''' 
    Display details and update book
    '''   
    # print("isbn is : ", isbn)
    current_book = Book.objects.filter(uuid=isbn).first()
    form = BookForm(request.POST or None, instance=current_book)
    if form.is_valid():
        form.save()
        return render(request, "detail.html", {'form' : form })
    # print('les titres sont : ', form)
    return render(request, "detail.html", {'form' : form })


def invite_new_user(request, email):
    ''' 
    invite new users to application
    '''  
    if request.method == "POST":
        Invitation = get_invitation_model()
        invite = Invitation.create(email, inviter=request.user)
        invite.send_invitation(request)
        return render(request, 'main.html')





def main(request):
    if request.method == "POST":
        print('post')        
        inviteform = InviteForm(request.POST)
        if inviteform.is_valid():
            print("valid")
            cleaned_email = inviteform.cleaned_data["post"]
            print("email is:", cleaned_email)
            invite_new_user(request,cleaned_email)
            return render(request, "main.html")
        return render(request, 'main.html')
    else:
        print('get')
        form = SearchForm(request.GET)
        inviteform =  InviteForm()
        print(inviteform)
        if form.is_valid():
            data = form.cleaned_data["post"].casefold()
            invite_data = inviteform
            print("invite", invite_data)
            # check if input is isbn number or title
            checked_input = input_cleaner(str(data))
            # search on title
            result = isbn_text_search(str(checked_input))
            request.session['temp_json'] = result
            context = {"form": form, "inviteform": invite_data, "result": result}
            return render(request, "main.html", context)    
        return render(request, "main.html", {"form": form, "inviteform": inviteform})