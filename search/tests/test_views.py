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
)
from django.shortcuts import get_object_or_404
from users.models import CustomUser
import requests

class MainPagetestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="toto@gmail.com", username="toto")

    # def test_main_post_page_returns_200(self):
    #     request = self.client.post(reverse("main"), kwargs={"post": "friend@yahoo.com"})
    #     request.user = self.user
    #     response = main(request)
    #     self.assertEquals(response.status_code, 200)

    def test_main_get_page_returns_200(self):
        response = self.client.get(
            reverse("main"), kwargs={"get": "poulet aux brocolis"}
        )
        self.assertEquals(response.status_code, 200)

    def test_input_cleaner_returns_string(self):
        # response = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:9782872620906')
        # response['items'][0]['volumeInfo']['title']
        result = input_cleaner(9782872620906)
        self.assertEquals(result,"Don Pablo et ses amis")

    # def test_request_response():
    #     # Send a request to the API server and store the response.
    #     response = requests.get('https://www.googleapis.com/books/v1/volumes?q=pablo')

    #     # Confirm that the request-response cycle completed successfully.
    #     assert_true(response.ok)