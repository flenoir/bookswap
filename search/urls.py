
from django.urls import path

# from .views import MainAppView, main
from . import views


urlpatterns = [
    path('', views.main, name = 'main'),
    path('save/<str:isbn>', views.save_book, name = 'save_book'),
    path('book_list/', views.book_list, name = 'book_list'),
]
