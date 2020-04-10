from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from users.models import CustomUser, Ownership, Borrowing
from django.urls import reverse_lazy
from .form import BookForm, SearchForm, InviteForm, RentForm
from invitations.utils import get_invitation_model
from django.core.mail import send_mail, EmailMessage
from django.db.models.functions import Now

import json
import requests
import dateparser


def google_api_request(words):
    """
    make a search on google books api
    """
    r = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + words)
    parsed = r.json()
    return parsed


def isbn_text_search(words):
    """
    make a search request based on title or authors
    """
    # r = requests.get('https://www.googleapis.com/books/v1/volumes?q='+ words)
    # parsed = r.json()
    parsed_words = google_api_request(words)
    # check if isbn identifier is not null
    for x in parsed_words["items"]:
        if "industryIdentifiers" not in x["volumeInfo"]:
            parsed_words["items"].remove(x)
        else:
            print("No ISBN number found")
    return parsed_words["items"]


def input_cleaner(search_data):
    """
    make a search request based on isbn number
    """
    try:
        if type(int(search_data)):
            res = requests.get(
                "https://www.googleapis.com/books/v1/volumes?q=isbn:" + str(search_data)
            )
            parsed_res = res.json()
            return parsed_res["items"][0]["volumeInfo"]["title"]
    except ValueError as error:
        print(error)
        return search_data


def save_book(request, isbn):
    """
    save book on book table
    """
    if request.method == "POST":
        data = request.session.get("temp_json")

        for i in data:
            if i["volumeInfo"]["industryIdentifiers"][0]["identifier"] == isbn:
                print("found match !")
                print("user is:", request.user.username)
                # search in user library if current user already owns the book
                user_library = [item.isbn for item in request.user.user_books.all()]
                if (
                    i["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                    not in user_library
                ):
                    # save book
                    try:
                        book = Book.objects.create(isbn=isbn)
                        book.isbn = i["volumeInfo"]["industryIdentifiers"][0][
                            "identifier"
                        ]
                        book.title = i["volumeInfo"]["title"]
                        book.author = i["volumeInfo"].get("authors", "...")
                        book.cover = i["volumeInfo"]["imageLinks"]["thumbnail"]
                        book.publisher = i["volumeInfo"].get("publisher", "...")
                        book.description = i["volumeInfo"].get("description", "...")
                        book.category = i["volumeInfo"].get(
                            "categories", "uncategorized"
                        )
                        book.page_count = i["volumeInfo"].get("pageCount", 0)
                        book.state = "good condition"
                        book.availability = True
                        cured_date = dateparser.parse(i["volumeInfo"]["publishedDate"])
                        book.published_date = cured_date.date()
                        book_status = Ownership(
                            book=book,
                            customuser=request.user,
                            state="Neuf",
                            availability=True,
                        )
                        book_status.save()
                        book.save()
                        print("je l'associe à l'utilisateur courant")
                        request.user.user_books.add(book)
                        print("saved")

                    except Exception as e:
                        print("not saved :", e)

            else:
                print("not matched")
                context = Book().book_search(request)
        return render(request, "book_list.html", context)
    else:
        print("save method had been called !")


# def book_search(request):
#     '''
#     select all uuid of current user book list
#     '''
#     books = CustomUser.objects.filter(user_books__isnull=False).filter(id=request.user.id)
#     if books:
#         main_book_list = [i for i in books]
#         sub_books = [j for j in main_book_list[0].user_books.all()]
#         return {"full_list": sub_books}
#     else:
#         return {"full_list": ""}


def remove_book(request, isbn):
    """
    remove book from user's list
    """
    if request.method == "POST":
        request.user.user_books.remove(isbn)
        context = Book().book_search(request)
        return render(request, "book_list.html", context)


def book_list(request):
    """
    list all books saved by an user
    """
    context = Book().book_search(request)
    return render(request, "book_list.html", context)


def book_detail(request, isbn):
    """
    Display details and update book
    """
    if request.method == "GET":  # peut-on simplifier/séparer les request GET et POST ?
        print("get")
        current_book = Book.objects.filter(uuid=isbn).first()
        book_owner = CustomUser.objects.filter(user_books__uuid=isbn).first()
        book_status = Ownership.objects.filter(
            book=current_book, customuser=book_owner
        ).first()
        print(book_status.state, book_status.availability)
        form = BookForm(request.POST or None, instance=current_book)
        rentform = RentForm()
        context = {
            "form": form,
            "current_book": current_book,
            "book_owner": book_owner,
            "rentform": rentform,
            "book_status": book_status,
        }
        if form.is_valid():
            form.save()
            return render(request, "detail.html", context)
        else:
            print("form is not valid")
        return render(request, "detail.html", context)
    else:
        print("post")
        current_book = Book.objects.filter(uuid=isbn).first()
        book_owner = CustomUser.objects.filter(user_books__uuid=isbn).first()
        form = BookForm(request.POST or None, instance=current_book)
        rentform = RentForm(
            request.POST
        )  # will put date values in database to book the books, they will be removed if owner refuses rental
        context = {
            "form": form,
            "current_book": current_book,
            "book_owner": book_owner,
            "rentform": rentform,
        }
        if rentform.is_valid():
            rental_request = Borrowing.objects.create(
                book=current_book,
                customuser=book_owner,
                start_date=rentform.cleaned_data["rent_start_field"],
                end_date=rentform.cleaned_data["rent_end_field"],
                rental_request_date=Now(),
            )

            # send an email to owner
            email = EmailMessage(
                "Demande de prêt du livre '"
                + current_book.title
                + "' via la plateforme Bookswap",
                "Bonjour, \n Je souhaiterais vous emprunter le livre '"
                + current_book.title
                + "'. \n Les dates que je vous proposent sont entre le "
                + str(rentform.cleaned_data["rent_start_field"])
                + " et "
                + str(rentform.cleaned_data["rent_end_field"])
                + ". Pouvez-vous vous connecter sur la plateforme sur votre compte afin de valider ma demande ? \n Merci \n"
                + str(request.user),
                request.user.email,  # idée d'ajouter un attribut sur un booleen qui est en état False, le propriétaire doit le valider et le passer en True pour valider l'échange. Le proriétaie peut aussi "rejecter" la demande " effacement des champs start et end + si demande pas traitée sous 2 jours, , on efface les champs start et end
                [book_owner.email],
                headers={"Reply-To": request.user.email},
            )
            email.send()
        return render(request, "detail.html", context)


def invite_new_user(request, email):
    """
    invite new users to application
    """
    Invitation = get_invitation_model()
    invite = Invitation.create(email, inviter=request.user)
    invite.send_invitation(request)
    return render(request, "main.html")


def exchange_request(request, title, ownersmail):
    """
    send request to owner for an exchange
    """
    # send_mail("Demande d'échange de livre via la plateforme Bookswap",
    # "Bonjour, \n Je souhaiterais échanger le livre '"+ title +"' avec vous, pouvez-vous vous connecter sur la plateforme sur mon compte afin de voir si vous trouvez un livre qui vous intéresse ?\n request.user",
    # "request.user",  #request.user
    # [ownersmail],
    # fail_silently=False,
    # )
    email = EmailMessage(
        "Demande d'échange de livre via la plateforme Bookswap",
        "Bonjour, \n Je souhaiterais échanger le livre '"
        + title
        + "' avec vous, pouvez-vous vous connecter sur la plateforme sur mon compte afin de voir si vous trouvez un livre qui vous intéresse ?\n "
        + str(request.user),
        request.user.email,  # request.user
        [ownersmail],
        headers={"Reply-To": request.user.email},
    )
    email.send()
    print(request, ownersmail, request.path)
    context = book_search(request)
    return render(request, "main.html", context)


# def get_all_users_books():
#     """
#     display entire bookswap library
#     """
#     library = Book.objects.all()
#     return library


def main(request):
    if request.method == "POST":
        inviteform = InviteForm(request.POST)
        if inviteform.is_valid():
            cleaned_email = inviteform.cleaned_data["post"]
            invite_new_user(request, cleaned_email)
            return render(request, "main.html")
        return render(request, "main.html")
    else:
        inviteform = InviteForm()
        library = Book().get_all_users_books()
        return render(
            request, "main.html", {"inviteform": inviteform, "library": library}
        )


def search_result(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data["post"].casefold()
        if data:
            # check if input is isbn number or title
            checked_input = input_cleaner(str(data))
            # search on title
            result = isbn_text_search(str(checked_input))
            request.session["temp_json"] = result
            context = {"form": form, "result": result}
            return render(request, "search_result.html", context)
        else:
            context = {"form": form}
            return render(request, "search_result.html", context)
