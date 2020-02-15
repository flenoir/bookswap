from django.test import TestCase
from search.models import Book
import uuid


class TestModels(TestCase):

    # Setup variable
    def setUp(self):
        self.book1 = Book.objects.create(
            uuid=uuid.uuid4(),
            isbn=97847775434226,
            title="my test book",
            author="the test author",
            cover="/images/test_cover.jpg",
            publisher="test publisher",
            description="test description",
            category="test category",
            state="test state",
            page_count=100,
            creation_date='2020-02-02',
            published_date='1978-06-13',
            availability=True,
        )
    
    # test book is created
    def test_Book_is_created(self):
        self.assertEquals(Book.objects.all().count(), 1)

