from django.contrib.auth.models import AbstractUser
from django.db import models
from search.models import Book
from pprint import pprint
from inspect import getmembers

STATE = (
    ('Neuf', 'Neuf'),
    ('Bon état', 'Bon état'),
    ('Légèrement abimé', 'Légèrement abimé'),
    ('Très abimé', 'Très abimé'),
)


class CustomUser(AbstractUser):
    user_books = models.ManyToManyField(Book, through='Ownership', related_name='owner')
    borrower = models.ManyToManyField(Book, through='Borrowing')
    friends = models.ManyToManyField("self")


    def book_search(self, request):
        '''
        select all uuid of current user book list
        '''
        books = Borrowing.objects.filter(customuser=request.user).select_related('book', 'customuser')
        if books:
            return {"full_list":books}
        else:
            return {"full_list": ""}

    def delete_book(self, request, uuid):
        """
        remove book from user's list
        """
        Book.remove(uuid)


class Ownership(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, null=True, choices=STATE )
    availability = models.BooleanField(null=True)


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date  = models.DateField(auto_now=False, null=True)
    end_date  = models.DateField(auto_now=False, null=True)
    rental_request_date  = models.DateField(auto_now=False, null=True)
    rental_validation = models.BooleanField(null=False, default=False)
    borrowing_user = models.CharField(null=True, max_length=100)

