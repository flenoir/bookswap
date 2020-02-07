
from django.urls import path

# from .views import MainAppView, main
from . import views


urlpatterns = [
    path('', views.main, name = 'main'),
    path('save/<str:isbn>/', views.save_book, name = 'save_book'),
    path('remove/<str:isbn>', views.remove_book, name = 'remove_book'),
    path('book_list/', views.book_list, name = 'book_list'),
    path('send_invite/', views.invite_new_user, name = 'invite_new_user'),
]
