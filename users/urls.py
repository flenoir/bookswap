from django.urls import path
from .views import SignUpView, UpdateUserView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit_user/<slug:pk>', UpdateUserView.as_view(), name="edit_user"),
]