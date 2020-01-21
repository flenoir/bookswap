
from django.urls import path

# from .views import MainAppView, main
from . import views


urlpatterns = [
    path('', views.main, name = 'main'),
]
