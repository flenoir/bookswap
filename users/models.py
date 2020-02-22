from django.contrib.auth.models import AbstractUser
from django.db import models
from search.models import Book


class CustomUser(AbstractUser):
    user_books = models.ManyToManyField(Book)
    friends = models.ManyToManyField("self")
