from django import forms

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
        )
        widget =  {
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

