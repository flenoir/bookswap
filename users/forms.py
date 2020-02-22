from django import forms
from django.forms import Textarea
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_books', 'friends')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = CustomUserCreationForm.Meta.fields
        widgets = {
            'username': Textarea(attrs={'cols': 30, 'rows': 1}),
            'date_joined': Textarea(attrs={'style': 'display:none;'}),
        }