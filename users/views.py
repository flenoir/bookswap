from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import CustomUser

from .forms import CustomUserCreationForm, CustomUserChangeForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class UpdateUserView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('main')
    template_name = 'edit_user.html'
    queryset = CustomUser.objects.all()