from django.test import TestCase
from django.urls import reverse
from search.models import Book
from search.views import (
    isbn_text_search,
    input_cleaner,
    save_book,
    book_search,
    remove_book,
    book_list,
    book_detail,
    invite_new_user,
    get_all_users_books,
    main,
    google_api_request,
)
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from django.db.models.query import QuerySet
import requests
import json
import uuid
from unittest import mock


class MainPagetestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="toto@gmail.com", username="toto")
        self.user.set_password("12345")
        self.user.save()
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
            creation_date="2020-02-02",
            published_date="1978-06-13",
            availability=True,
        )
        self.book2 = Book.objects.create(
            uuid=uuid.uuid4(),
            isbn=97847775438250,
            title="my second test book",
            author="another test author",
            cover="/images/test_cover_second_book.jpg",
            publisher="test second publisher",
            description="test second description",
            category="test second category",
            state="test second state",
            page_count=200,
            creation_date="2019-08-10",
            published_date="1990-03-09",
            availability=True,
        )
        self.user.user_books.add(self.book2)
        # fixtures = ['../fixtures/isbn_api_data.json']

    def test_main_page_display_all_user_books(self):
        response = self.client.get(reverse("main"))
        self.failUnless(isinstance(response.context["library"], QuerySet))
        self.assertTemplateUsed(response, "main.html")
        self.failUnlessEqual(response.status_code, 200)

    def test_main_get_page_returns_200(self):
        response = self.client.get(
            reverse("main"), kwargs={"get": "poulet aux brocolis"}
        )
        self.assertEquals(response.status_code, 200)

    # def test_isbn_text_search(self):
    #     # response = requests.get('https://www.googleapis.com/books/v1/volumes?q=pablo')
    #     # parsed = json.loads(response.text)
    #     response = isbn_text_search("pablo")
    #     self.assertEquals(response[0]["volumeInfo"]["title"], "Pablo de la Courneuve")

    # def test_input_cleaner_returns_string(self):
    #     result = input_cleaner(9782872620906)
    #     self.assertEquals(result, "Don Pablo et ses amis")

    def test_input_cleaner_returns_ValueError(self):
        result = input_cleaner("pablo")
        self.assertEquals(result, "pablo")

    def test_book_remove(self):
        self.client.login(username="toto", password="12345")
        response = self.client.post(reverse("remove_book", args=(self.book2.uuid,)))
        self.assertEquals(len(response.context["full_list"]), 0)
        self.assertTemplateUsed(response, "book_list.html")
        self.failUnlessEqual(response.status_code, 200)

    # def test_save_book(self):
    #     self.client.login(username="toto", password="12345")
    #     response = self.client.post(reverse("save_book", args=(self.book1.uuid,)))
    #     print(response.context)

    @mock.patch("search.views.requests.get")
    def test_isbn_text_search_return(self, mock_get):
        mock_get.return_value.json.return_value = {
            "items": {
                    "kind": "books#volume",
                    "id": "RjOB6wq3Y3MC",
                    "etag": "DYk6HRNSWc8",
                    "selfLink": "https://www.googleapis.com/books/v1/volumes/RjOB6wq3Y3MC",
                    "volumeInfo": {
                        "title": "Don Pablo et ses amis",
                        "publisher": "Editions Aden",
                        "publishedDate": "1994-05-01",
                        "industryIdentifiers": [
                            {"type": "ISBN_10", "identifier": "2872620907"},
                            {"type": "ISBN_13", "identifier": "9782872620906"},
                        ],
                        "readingModes": {"text": False, "image": True},
                        "pageCount": 184,
                        "printType": "BOOK",
                        "categories": ["Cocaine industry"],
                        "maturityRating": "NOT_MATURE",
                        "allowAnonLogging": False,
                        "contentVersion": "0.0.1.0.preview.1",
                        "imageLinks": {
                            "smallThumbnail": "http://books.google.com/books/content?id=RjOB6wq3Y3MC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api",
                            "thumbnail": "http://books.google.com/books/content?id=RjOB6wq3Y3MC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                        },
                        "language": "fr",
                        "previewLink": "http://books.google.fr/books?id=RjOB6wq3Y3MC&printsec=frontcover&dq=isbn:9782872620906&hl=&cd=1&source=gbs_api",
                        "infoLink": "http://books.google.fr/books?id=RjOB6wq3Y3MC&dq=isbn:9782872620906&hl=&source=gbs_api",
                        "canonicalVolumeLink": "https://books.google.com/books/about/Don_Pablo_et_ses_amis.html?hl=&id=RjOB6wq3Y3MC",
                    },
                    "saleInfo": {
                        "country": "FR",
                        "saleability": "NOT_FOR_SALE",
                        "isEbook": False,
                    },
                    "accessInfo": {
                        "country": "FR",
                        "viewability": "PARTIAL",
                        "embeddable": True,
                        "publicDomain": False,
                        "textToSpeechPermission": "ALLOWED",
                        "epub": {"isAvailable": False},
                        "pdf": {"isAvailable": False},
                        "webReaderLink": "http://play.google.com/books/reader?id=RjOB6wq3Y3MC&hl=&printsec=frontcover&source=gbs_api",
                        "accessViewStatus": "SAMPLE",
                        "quoteSharingAllowed": False,
                    }
            }
        }
        response = google_api_request("pablo")
        self.assertEquals(response, mock_get.return_value.json.return_value)

    @mock.patch('search.views.requests.get')
    def test_input_cleaner_mock(self, mock_get):
        # print(mock_get.return_value.json.return_value)
        mock_get.return_value.json.return_value = {
            "items": [{
                    "volumeInfo": {
                        "title": "Don Pablo et ses amis",
                        "publisher": "Editions Aden",
                        "publishedDate": "1994-05-01",
                        "industryIdentifiers": [
                            {"type": "ISBN_10", "identifier": "2872620907"},
                            {"type": "ISBN_13", "identifier": "9782872620906"},
                        ],
                        "readingModes": {"text": False, "image": True},
                        "pageCount": 184,
                        "printType": "BOOK",
                        "categories": ["Cocaine industry"],
                        "maturityRating": "NOT_MATURE",
                        "allowAnonLogging": False,
                        "contentVersion": "0.0.1.0.preview.1",
                        "imageLinks": {
                            "smallThumbnail": "http://books.google.com/books/content?id=RjOB6wq3Y3MC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api",
                            "thumbnail": "http://books.google.com/books/content?id=RjOB6wq3Y3MC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
                        },
                        "language": "fr",
                        "previewLink": "http://books.google.fr/books?id=RjOB6wq3Y3MC&printsec=frontcover&dq=isbn:9782872620906&hl=&cd=1&source=gbs_api",
                        "infoLink": "http://books.google.fr/books?id=RjOB6wq3Y3MC&dq=isbn:9782872620906&hl=&source=gbs_api",
                        "canonicalVolumeLink": "https://books.google.com/books/about/Don_Pablo_et_ses_amis.html?hl=&id=RjOB6wq3Y3MC",
                    },              
            }]
        }
        response = input_cleaner(9782872620906)
        self.assertEquals(response,mock_get.return_value.json.return_value['items'][0]['volumeInfo']['title'])

    def test_book_search(self):
        result = book_search(self)
        self.assertEquals(len(result), 1)
