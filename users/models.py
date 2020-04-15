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

    def book_search(self):
        # sub_books = Borrowing.objects.filter(customuser=self.pk).exclude(start_date=None).values('start_date', 'book__title', 'customuser__email')
        sub_books = Borrowing.objects.filter(customuser=self.pk).exclude(start_date=None)
        return {"full_list": sub_books}

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

