from django.test import TestCase
from search.form import SearchForm, InviteForm

class FormTests(TestCase):

    # test search form is valid
    def test_search_form_is_valid(self):
        form_data = {"post": "un sac de billes"}
        form = SearchForm(form_data)
        self.assertTrue(form.is_valid())
    
    # test invite form is valid
    def test_invite_form_is_valid(self):
        form_data = {"post": "foo@bar.com"}
        form = InviteForm(form_data)
        self.assertTrue(form.is_valid())

