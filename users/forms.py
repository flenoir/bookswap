from django import forms
from django.forms import Textarea
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_books', 'friends')

class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Row(
        #         Column("username", css_class="form-group col-md-6 mb-0"),
        #         Column("email", css_class="form-group col-md-6 mb-0"),
        #         css_class="form-row",
        #     ),
        #     Row(
        #         Column("first_name", css_class="form-group col-md-6 mb-0"),
        #         Column("last_name", css_class="form-group col-md-6 mb-0"),
        #         css_class="form-row",
        #     ),
        #     Row(
        #         Column("user_books", css_class="form-group col-md-8 mb-0"),
        #         Column("friends", css_class="form-group col-md-4 mb-0"),
        #         css_class="form-row",
        #     ),
        #     "password",
        #     Submit("submit", "Update User"),
        # )
        self.helper.layout = Layout(
            Row(
                Column("username", css_class="grid-cols-6 mr-3"),
                Column("email", css_class="grid-cols-6"),
                css_class="form-row",
            ),
            Row(
                Column("first_name", css_class="grid-cols-6 mr-3"),
                Column("last_name", css_class="grid-cols-6"),
                css_class="form-row",
            ),
            Row(
                Column("user_books", css_class="grid-cols-6 mr-2"),
                Column("friends", css_class="grid-cols-4"),
                css_class="form-row",
            ),
            "password",
            Submit("submit", "Update User"),
        )


    class Meta:
        model = CustomUser
        fields = CustomUserCreationForm.Meta.fields
        widgets = {
            'username': Textarea(attrs={'cols': 30, 'rows': 1}),
            'date_joined': Textarea(attrs={'style': 'display:none;'}),
        }