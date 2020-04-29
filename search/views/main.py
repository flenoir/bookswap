from django.shortcuts import render
from ..form import InviteForm
from ..models import Book
from .sharing import invite_new_user

def main(request):
    if request.method == "POST":
        inviteform = InviteForm(request.POST)
        if inviteform.is_valid():
            cleaned_email = inviteform.cleaned_data["post"]
            invite_new_user(request, cleaned_email)
            return render(request, "main.html")
        return render(request, "main.html")
    else:
        inviteform = InviteForm()
        library = Book().get_all_users_books()
        return render(
            request, "main.html", {"inviteform": inviteform, "library": library}
        )