from django.shortcuts import render
from ..models import Book
from users.models import CustomUser, Ownership, Borrowing
from ..form import BookForm, RentForm
from django.core.mail import EmailMessage
from django.db.models.functions import Now



def book_detail(request, isbn):
    """
    Display details of non-owned books
    """
    if request.method == "GET":  # peut-on simplifier/séparer les request GET et POST ?
        print("get")
        current_book = Book.objects.filter(uuid=isbn).first()
        book_owner = CustomUser.objects.filter(user_books__uuid=isbn).first()
        book_status = Ownership.objects.filter(
            book=current_book, customuser=book_owner
        ).first()
        rental_request = Borrowing.objects.filter(
            book=current_book, customuser=book_owner,
        ).first()

        rentform = RentForm()
        if rental_request:
            context = {
                "current_book": current_book,
                "book_owner": book_owner,
                "rentform": rentform,
                "book_status": book_status,
                "rental_start": rental_request.start_date,
                "rental_end": rental_request.end_date,
            }
        else:
            context = {
                "current_book": current_book,
                "book_owner": book_owner,
                "rentform": rentform,
                "book_status": book_status,
            }

        return render(request, "detail.html", context)
    else:
        print("post")
        current_book = Book.objects.filter(uuid=isbn).first()
        book_owner = CustomUser.objects.filter(user_books__uuid=isbn).first()
        form = BookForm(request.POST or None, instance=current_book)
        if form.is_valid():
            form.save()
            return render(request, "detail.html", context)
        else:
            print("form is not valid")
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
            objToUpdate = Borrowing.objects.filter(
                book=current_book.uuid, customuser=book_owner.id
            ).update(
                start_date=rentform.cleaned_data["rent_start_field"],
                end_date=rentform.cleaned_data["rent_end_field"],
                rental_request_date=Now(),
                borrowing_user=request.user.id,
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
                request.user.email,
                [book_owner.email],
                headers={"Reply-To": request.user.email},
            )
            email.send()
        return render(request, "detail.html", context)

def book_owner_detail(request, isbn):
    """
    Display owned books details and update book
    """
    if request.method == "GET":  # peut-on simplifier/séparer les request GET et POST ?
        print("get")
        current_book = Book.objects.filter(uuid=isbn).first()
        book_owner = CustomUser.objects.filter(user_books__uuid=isbn).first()
        book_status = Ownership.objects.filter(
            book=current_book, customuser=book_owner
        ).first()
        rental_request = Borrowing.objects.filter(
            book=current_book, customuser=book_owner,
        ).first()

        form = BookForm(request.POST or None, instance=current_book)
        if rental_request:
            context = {
                "form": form,
                "current_book": current_book,
                "book_owner": book_owner,
                "book_status": book_status,
            }
        else:
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
        form.save()
        context = {
            "form": form,
            "current_book": current_book,
            "book_owner": book_owner,
        }

        return render(request, "detail.html", context)
