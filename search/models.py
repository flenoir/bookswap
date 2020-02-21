from django.db import models
import uuid

# Create your models here.

STATE = (  
    ('Neuf', 'Neuf'),
    ('Bon état', 'Bon état'),
    ('Légèrement abimé', 'Légèrement abimé'),
    ('Très abimé', 'Très abimé'),

)


class Book(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    isbn  = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    cover = models.CharField(max_length=300, null=True)
    publisher = models.CharField(max_length=150, null=True)
    description = models.TextField(null=True)
    category = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=50, null=True, choices=STATE )
    page_count = models.PositiveSmallIntegerField(null=True)
    creation_date = models.DateTimeField(auto_now=True)
    published_date  = models.DateField(auto_now=False, null=True)
    availability = models.BooleanField(null=True)
    
    def  __str__(self):
        return self.title