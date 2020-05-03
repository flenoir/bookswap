from django.shortcuts import render
from ..models import Book
from users.models import CustomUser, Ownership, Borrowing
import dateparser
from datetime import date


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
                        request.user.borrower.add(book)

                        print("saved")

                    except Exception as e:
                        print("not saved :", e)

            else:
                print("not matched")
                context = request.user.book_search(request)
        return render(request, "book_list.html", context)
    else:
        print("save method had been called !")


def remove_book(request, isbn):
    """
    remove book from user's list
    """
    if request.method == "POST":
        request.user.delete_book(request, isbn)
        context = request.user.book_search(request)
        return render(request, "book_list.html", context)

def check_availability_routine():
    all_borrowed_books = Borrowing.objects.all()
    today = date.today()
    for item in all_borrowed_books:
        if item.start_date <= today <= item.end_date:
            print("in range", item.start_date, item.end_date )
        else:
            print("not in range", item.start_date, item.end_date )
            print(item.book.uuid, item.customuser.id )
            Book.objects.filter(uuid=item.book.uuid
                ).update(
                    availability=True,
                )
            Borrowing.objects.filter(book=item.book.uuid, customuser=item.customuser.id
                ).update(
                    rental_validation=False,
                )


def book_list(request):
    """
    list all books saved by an user
    """
    check_availability_routine()
    context = request.user.book_search(request)
    return render(request, "book_list.html", context)


