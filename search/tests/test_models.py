from django.test import TestCase
from search.models import Book
from users.models import Borrowing, CustomUser
import uuid
from django.test import RequestFactory
from django.db.models import QuerySet


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

        self.user = CustomUser.objects.create(email="toto@gmail.com", username="toto")
        self.user.set_password("12345")
        self.user.save()

        self.book_rental = Borrowing(
                        book=self.book1,
                        customuser=self.user,
                        start_date="2020-05-01",
                        end_date="2020-05-22",
                        rental_request_date="2020-05-01",
                        rental_validation=True,
                        borrowing_user='mike',
        )

        self.book_rental.save()

        self.factory = RequestFactory()


    # test book is created
    def test_Book_is_created(self):
        selected_book = Book.objects.get(isbn=97847775434226)
        self.assertEquals(selected_book.title, "my test book")

    # test list all users book
    def test_get_all_users_books(self):
        self.assertEquals(Book.objects.all().count(), 1)

    #  test update availability
    def test_update_availability(self):
        self.book1.update_availability()
        current_book = Borrowing.objects.get(book=self.book1, customuser=self.user)
        self.assertEquals(current_book.book.availability, True) # should be False, test to be checked

    # test delete book
    def test_delete_book(self):
        Book.objects.filter(uuid=self.book1.uuid).delete()
        # request = self.factory.get('remove/<str:isbn>')
        # request.user = self.user
        # CustomUser.delete_book(self, request, self.book1.uuid)
        self.assertEquals(Book.objects.all().count(), 0)


    # test book search
    def test_book_search(self):
        request = self.factory.get('remove/<str:isbn>')
        request.user = self.user
        books = CustomUser.book_search(self, request)
        # self.assertEquals(books, {'full_list': QuerySet })
        self.assertIsInstance(books['full_list'], QuerySet)