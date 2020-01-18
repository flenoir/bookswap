from django.db import models
import uuid

# Create your models here.


class Book(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    isbn  = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    
    def  __str__(self):
        return self.title