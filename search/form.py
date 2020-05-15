from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Submit,
    Row,
    Column,
    HTML,
    Div,
    Field,
    Fieldset,
    ButtonHolder,
)

from .models import Book


class BookForm(forms.ModelForm):

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
            "publisher",
            "rating",
        )
        labels = {
            "title": "Titre",
            "author": "Auteurs",
            "availability": "Disponibilité",
            "category": "Categorie",
            "cover": "Couverture",
            "description": "Description",
            "state": "Etat",
            "publisher": "Editeur",
            "rating": "Avis",
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
            attrs={"placeholder": "email de la personne à inviter", "size": "40",}
        ),
    )

class DateInput(forms.DateInput):
    input_type = 'date'

class RentForm(forms.Form):
    rent_start_field = forms.DateField(
        label="début d'emprunt",
        required=False,
        # widget=forms.TextInput(attrs={"placeholder": "début d'emprunt", "size": "20",}),
        widget=DateInput,
    )
    rent_end_field = forms.DateField(
        label="fin d'emprunt",
        required=False,
        # widget=forms.TextInput(attrs={"placeholder": "fin d'emprunt", "size": "20",}),
        widget=DateInput,
    )
