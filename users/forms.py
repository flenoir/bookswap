from django import forms
from django.forms import Textarea
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, ButtonHolder, Div, Fieldset, Field

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_books', 'friends')

class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()   
        self.helper.layout = Layout( 
            Div(
                Fieldset('', 'username','email', 'first_name', 'last-name', 'user_books', 'friends'),                
                Div("password", css_class="invisible my-1 px-1 w-1/2 overflow-hidden"),
                Div(ButtonHolder(
                    Submit("submit", "Update User", css_class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),                
                ), css_class="my-1 px-1 w-1/2 overflow-hidden"),
                css_class="flex flex-wrap -mx-2 overflow-hidden"
            )
        )


    class Meta:
        model = CustomUser
        fields = CustomUserCreationForm.Meta.fields
        widgets = {
            'username': Textarea(attrs={'cols': 30, 'rows': 1}),
            'date_joined': Textarea(attrs={'style': 'display:none;'}),
        }