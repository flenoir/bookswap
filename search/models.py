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

RATING = (
    (0, "Je n'ai pas aimé"),
    (1, "Bof, sans plus"),
    (2, "A lire"),
    (3, "Bon livre"),
    (4, "Je recommande"),
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
    rating = models.PositiveSmallIntegerField(null=True, choices=RATING)

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

    def get_all_users_books(self):
        """
        display entire bookswap library
        """
        library = Book.objects.all()
        return library
