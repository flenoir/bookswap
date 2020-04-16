from django.contrib.auth.models import AbstractUser
from django.db import models
from search.models import Book

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
        books = CustomUser.objects.filter(user_books__isnull=False).filter(id=request.user.id)
        # book_rental_status = Borrowing.objects.filter(book=current_book, customuser=request.user).first()
        print(books)
        if books:
            # sub_books = Borrowing.objects.filter(customuser=self.pk)
            sub_books = Ownership.objects.filter(customuser=self.pk)
            print("sub", sub_books)
            return {"full_list": sub_books}
        else:
            return {"full_list": ""}

    def delete_book(self, request, uuid):
        """
        remove book from user's list
        """
        request.user.user_books.remove(uuid)
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

