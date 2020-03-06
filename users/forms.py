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
                # HTML('<div class="mb-4"><label class="block text-gray-700 text-sm font-bold mb-2" for="username"></label><input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username" value="{{form.username.value}}"></div>'),             
                Div("password", css_class="invisible my-1 px-1 w-1/2 overflow-hidden"),
                Div(ButtonHolder(
                    Submit("submit", "Update User", css_class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),                
                ), css_class="my-1 px-1 w-1/2 overflow-hidden"),

                # Div(
                #     Div("username", css_class="w-1/2 h-20 px-2"),
                #     Div("email", css_class="w-1/2 h-20 px-2"),
                #     css_class="flex mb-4",
                # ),
                # Div(
                #     Div("first_name", css_class="w-1/2 h-12 px-2"),
                #     Div("last_name", css_class="w-1/2 h-12 px-2"),
                #     css_class="flex mb-4",
                # ),
                # Div(
                #     Div("user_books", css_class="flex-1 h-12 px-2"),
                #     # Div("friends", css_class="flex-1 h-12 px-2"),
                #     css_class="flex mb-4",
                # ),
                # Div(
                #     Div("friends", css_class="w-3/4 h-12 px-2 mt-2 mb-2"),
                #     Div("password", css_class="invisible flex-1 h-12"),
                #     css_class="flex-1 mb-4 mt-4"
                # ),
                # ButtonHolder(
                #     Submit("submit", "Update User", css_class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),                
                # ),
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