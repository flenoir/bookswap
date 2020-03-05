from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

from .models import Book


class BookForm(forms.ModelForm):

    # Supercharge form initialization
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "title",
            Row(
                Column("author", css_class="form-group col-md-6 mb-0"),
                Column("publisher", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            "description",
            Row(
                Column("isbn", css_class="form-group col-md-6 mb-0"),
                Column("cover", css_class="form-group col-md-6 mb-0"),
                # HTML('<img src="{{ "cover" }}"/>'),
                css_class="form-row",
            ),
            Row(
                Column("category", css_class="form-group col-md-6 mb-0"),
                Column("availability", css_class="form-group col-md-4 mb-0"),
                Column("state", css_class="form-group col-md-2 mb-0"),
                css_class="form-row",
            ),
            Submit("submit", "Update"),
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

