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

    # # Supercharge form initialization
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Div(                
    #             Field("title", css_class="w-full"),
    #             Div(
    #                 Field("author", css_class="my-1 px-1 w-1/2 overflow-hidden"),
    #                 Field("publisher", css_class="my-1 px-1 w-1/2 overflow-hidden"),
    #             ),
    #             Field("description", css_class="w-full"),
    #             Div(
    #                 Field("isbn", css_class="my-1 px-1 w-1/2 overflow-hidden"),
    #                 Field("cover", css_class="my-1 px-1 w-1/2 overflow-hidden"),
    #                 # HTML('<img src="{{ "cover" }}"/>'),
    #             ),
    #             Div(
    #                 Field("category", css_class="my-1 px-1 w-1/3 overflow-hidden"),
    #                 Field("availability", css_class="my-1 px-1 w-1/3 overflow-hidden"),
    #                 Field("state", css_class="my-1 px-1 w-1/3 overflow-hidden"),
    #             ),
    #             Div(
    #                 ButtonHolder(
    #                     Submit(
    #                         "submit",
    #                         "Update",
    #                         css_class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded",
    #                     ),
    #                 ),
    #             ),                
    #         )
    #     )

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
        )
        widgets = {
            "state": forms.Select(choices=[("neuf", "neuf"), ("bon état", "bon état")])
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

