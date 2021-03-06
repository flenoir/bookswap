
from django.urls import path

# from .views import MainAppView, main
from . import views


urlpatterns = [
    path('', views.main, name = 'main'),
    path('save/<str:isbn>/', views.save_book, name = 'save_book'),
    path('remove/<str:isbn>', views.remove_book, name = 'remove_book'),
    path('book_list/', views.book_list, name = 'book_list'),
    path('detail/<str:isbn>', views.book_detail, name = 'book_detail'),
    path('owner_detail/<str:isbn>', views.book_owner_detail, name = 'book_owner_detail'),
    path('validation/<str:title>/<str:isbn>', views.book_rental_validation, name = 'validate_rental'),
    path('send_invite/', views.invite_new_user, name = 'invite_new_user'),
    path('search_result/', views.search_result, name = "search_result"),
    path('exchange_request/<str:title>/<str:ownersmail>', views.exchange_request, name = "exchange_request"),
]
