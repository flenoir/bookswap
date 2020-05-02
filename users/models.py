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
        # from users.models import CustomUser # beware of circular import
        # from users.models import CustomUser, Ownership, Borrowing
        # current_customer = CustomUser.objects.filter(id=request.user.id)
        # books = Book.objects.filter(owner__id=request.user.id)
        books = Borrowing.objects.filter(customuser=self.pk).select_related('book', 'customuser')
        # book_rental_status = Borrowing.objects.filter(book=current_book, customuser=request.user).first()
        # print("l'utilisateur est: ", books)

        if books:
            # sub_books = Borrowing.objects.filter(customuser=self.pk)
            # owned_books = Borrowing.objects.filter(customuser=self.pk).select_related('book', 'customuser')
            # # print("sub", owned_books)
            # for b in books:
            #     pprint(getmembers(b.owner))
                # print(b.borrowing_set.select_related())

            return {"full_list":books}
        else:
            return {"full_list": ""}

    def delete_book(self, request, uuid):
        """
        remove book from user's list
        """
        request.user.borrower.remove(uuid)
        # print(request.user_books.all(), uuid)


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

