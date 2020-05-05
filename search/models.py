from django.db import models
from datetime import date
import uuid


# Create your models here.

STATE = (
    ("Neuf", "Neuf"),
    ("Bon état", "Bon état"),
    ("Légèrement abimé", "Légèrement abimé"),
    ("Très abimé", "Très abimé"),
)


class Book(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False
    )
    isbn = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    cover = models.CharField(max_length=300, null=True)
    publisher = models.CharField(max_length=150, null=True)
    description = models.TextField(null=True)
    category = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=50, null=True, choices=STATE)
    page_count = models.PositiveSmallIntegerField(null=True)
    creation_date = models.DateTimeField(auto_now=True)
    published_date = models.DateField(auto_now=False, null=True)
    availability = models.BooleanField(null=True)

    def __str__(self):
        return self.title


    def update_availability(self):
        """
        update availability when there's a new book rental request validated
        """
        from users.models import Borrowing
        from search.models import Book
        query = Borrowing.objects.filter(start_date__lte=date.today(),end_date__gte=date.today(),rental_validation=True).select_related('book')
        for b in query:
            Book.objects.filter(uuid=b.book.uuid).update(availability=False)

    # def book_search(self, request):
    #     '''
    #     select all uuid of current user book list
    #     '''
    #     from users.models import CustomUser # beware of circular import
    #     from users.models import CustomUser, Ownership, Borrowing
    #     books = CustomUser.objects.filter(user_books__isnull=False).filter(id=request.user.id)
    #     # book_rental_status = Borrowing.objects.filter(book=current_book, customuser=request.user).first()
    #     if books:
    #         main_book_list = list(books)
    #         print("main_book_list", main_book_list)
    #         sub_books = [j for j in main_book_list[0].user_books.all()]
    #         print("sub_books_list", sub_books)
    #         book_rental_status = [Borrowing.objects.filter(book=item, customuser=request.user).first() for item in sub_books]
    #         # Borrowing.objects.filter(book__in= sub_books, customuser=request.user).first()
    #         # for item in sub_books:
    #         #     book_rental_status = Borrowing.objects.filter(book=item, customuser=request.user).first()
    #         #     if book_rental_status != None:
    #         #         print("item", book_rental_status.start_date)
    #         #         return book_rental_status
    #         #     else:
    #         #         print("None")

    #         return {"full_list": sub_books, "rental_list": book_rental_status}
    #     else:
    #         return {"full_list": ""}

    def get_all_users_books(self):
        """
        display entire bookswap library
        """
        library = Book.objects.all()
        return library
