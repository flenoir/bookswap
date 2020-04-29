from django.shortcuts import render
from django.core.mail import EmailMessage
from ..models import Book
from users.models import Borrowing
from invitations.utils import get_invitation_model

def book_rental_validation(request, isbn):
    current_book = Book.objects.filter(uuid=isbn).first()
    # book_owner = CustomUser.objects.filter(user_books__uuid=isbn).first()
    book_owner = current_book.owner.first()
    Borrowing.objects.filter(
                book=current_book.uuid, customuser=book_owner.id
            ).update(
                rental_validation=True,
            )
    # 1 envoyer mail d'accord d'emprunt
    current_book.update_availability()
    context = request.user.book_search(request)
    return render(request, "book_list.html", context)


def invite_new_user(request, email):
    """
    invite new users to application
    """
    Invitation = get_invitation_model()
    invite = Invitation.create(email, inviter=request.user)
    invite.send_invitation(request)
    return render(request, "main.html")


def exchange_request(request, title, ownersmail):
    """
    send request to owner for an exchange
    """
    # send_mail("Demande d'échange de livre via la plateforme Bookswap",
    # "Bonjour, \n Je souhaiterais échanger le livre '"+ title +"' avec vous, pouvez-vous vous connecter sur la plateforme sur mon compte afin de voir si vous trouvez un livre qui vous intéresse ?\n request.user",
    # "request.user",  #request.user
    # [ownersmail],
    # fail_silently=False,
    # )
    email = EmailMessage(
        "Demande d'échange de livre via la plateforme Bookswap",
        "Bonjour, \n Je souhaiterais échanger le livre '"
        + title
        + "' avec vous, pouvez-vous vous connecter sur la plateforme sur mon compte afin de voir si vous trouvez un livre qui vous intéresse ?\n "
        + str(request.user),
        request.user.email,  # request.user
        [ownersmail],
        headers={"Reply-To": request.user.email},
    )
    email.send()
    print(request, ownersmail, request.path)
    context = request.user.book_search(request)
    return render(request, "main.html", context)

