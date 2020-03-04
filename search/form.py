from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import Book


class BookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('isbn', css_class='form-group col-md-6 mb-0'),
                Column('title', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'author',
            'availability',
            Row(
                Column('category', css_class='form-group col-md-6 mb-0'),
                Column('description', css_class='form-group col-md-4 mb-0'),
                Column('state', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'check_me_out',
            Submit('submit', 'Sign in')
        )


    class Meta:
        model = Book
        fields = (
            "isbn",
            "title",
            "author",
            "availability",
            "category",
            "cover",
            "description",
            "state",
        )
        widgets =  {
            'state': forms.Select(choices=[('neuf', 'neuf'),('bon état', 'bon état')])
        }


class SearchForm(forms.Form):
    post = forms.CharField(
        label="",
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "entrez ici le code ISBN, le titre ou l'auteur",
                "size": "100",
            }
        ),
    )


class InviteForm(forms.Form):
    post = forms.CharField(
        label="",
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": "email de la personne à inviter",
                "size": "40",
            }
        ),
    )

